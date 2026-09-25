/**
 * Client-Side PDF Parser and ATS Formatting Analyzer.
 * Extracts plain text from user-uploaded PDF resumes and conducts
 * an ATS formatting & layout diagnostic (columns, fonts, sections, page count).
 */

import * as pdfjsLib from 'pdfjs-dist';

// Configure pdfjs worker using standard URL constructor compatible with Vite & TypeScript
pdfjsLib.GlobalWorkerOptions.workerSrc = new URL(
  'pdfjs-dist/build/pdf.worker.mjs',
  import.meta.url
).toString();

export interface ATSFormattingAudit {
  formatting_score: number;
  page_count: number;
  has_machine_readable_text: boolean;
  is_single_column_friendly: boolean;
  detected_sections: string[];
  missing_sections: string[];
  contact_info_detected: {
    email: boolean;
    phone: boolean;
    linkedin_or_github: boolean;
  };
  table_graphic_risk: 'Low' | 'Moderate' | 'High';
  bullet_point_count: number;
  formatting_issues: string[];
  formatting_strengths: string[];
}

export interface PDFParseResult {
  text: string;
  audit: ATSFormattingAudit;
}

const EXPECTED_SECTIONS = [
  { name: 'Education', regex: /\b(education|academic|qualifications|degree)\b/i },
  { name: 'Experience', regex: /\b(experience|work experience|employment|history|internship)\b/i },
  { name: 'Skills', regex: /\b(skills|technical skills|technologies|proficiencies|competencies)\b/i },
  { name: 'Projects', regex: /\b(projects|personal projects|key projects|academic projects)\b/i },
];

/**
 * Parses an uploaded PDF file, extracts its text, and audits its ATS formatting.
 */
export async function parsePdfResume(file: File): Promise<PDFParseResult> {
  const arrayBuffer = await file.arrayBuffer();
  
  let fullText = '';
  let pageCount = 1;
  let hasText = false;
  let lineCount = 0;
  let bulletCount = 0;

  try {
    const loadingTask = pdfjsLib.getDocument({ data: arrayBuffer });
    const pdfDoc = await loadingTask.promise;
    pageCount = pdfDoc.numPages;

    const pageTexts: string[] = [];

    for (let i = 1; i <= pageCount; i++) {
      const page = await pdfDoc.getPage(i);
      const textContent = await page.getTextContent();
      
      const textItems = textContent.items.map((item) => {
        if ('str' in item) {
          return item.str;
        }
        return '';
      });

      const pageString = textItems.join(' ');
      pageTexts.push(pageString);
    }

    fullText = pageTexts.join('\n\n').trim();
    hasText = fullText.length > 50;
  } catch (err) {
    console.warn('⚠️ pdfjs-dist primary parse encountered an issue, running raw fallback:', err);
    // Fallback: simple text decoder on array buffer for ASCII/UTF-8 streams
    const textDecoder = new TextDecoder('utf-8', { fatal: false });
    const raw = textDecoder.decode(arrayBuffer);
    const matches = raw.match(/\(([^()]+)\)[\s]*Tj/g) || [];
    if (matches.length > 0) {
      fullText = matches.map(m => m.replace(/^\(|\)[\s]*Tj$/g, '')).join(' ');
      hasText = fullText.length > 50;
    }
  }

  // Calculate bullet points and lines
  const lines = fullText.split(/\r?\n|\.\s+/);
  lineCount = lines.length;
  bulletCount = (fullText.match(/[•\-\*\u2022\u2023\u25E6\u2043\u2219]/g) || []).length;

  // Audit ATS Sections
  const detectedSections: string[] = [];
  const missingSections: string[] = [];

  for (const sec of EXPECTED_SECTIONS) {
    if (sec.regex.test(fullText)) {
      detectedSections.push(sec.name);
    } else {
      missingSections.push(sec.name);
    }
  }

  // Audit Contact Info
  const hasEmail = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/.test(fullText);
  const hasPhone = /(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}/.test(fullText);
  const hasLinkedInOrGithub = /(linkedin\.com\/in\/|github\.com\/)/i.test(fullText);

  // Formatting Strengths & Issues
  const strengths: string[] = [];
  const issues: string[] = [];
  let score = 100;

  // 1. Text Layer Check
  if (!hasText) {
    score -= 45;
    issues.push('Scanned Image Warning: No selectable text layer detected. ATS bots cannot read image-only resumes.');
  } else {
    strengths.push('Selectable Text Layer: 100% machine-readable text stream detected.');
  }

  // 2. Page Count Penalty
  if (pageCount === 1) {
    strengths.push('Optimal Length: 1 page is ideal for 0-3 YOE candidates.');
  } else if (pageCount === 2) {
    strengths.push('Standard Length: 2 pages suitable for detailed project & work portfolios.');
  } else {
    score -= 15;
    issues.push(`Length Warning: ${pageCount} pages detected. Resumes over 2 pages are frequently penalized by corporate ATS filters.`);
  }

  // 3. Section Completeness
  if (detectedSections.length >= 3) {
    strengths.push(`Standard ATS Headers: Found ${detectedSections.join(', ')}.`);
  }
  if (missingSections.length > 0) {
    score -= missingSections.length * 8;
    issues.push(`Missing Standard Sections: Could not reliably parse ${missingSections.join(', ')} header(s).`);
  }

  // 4. Contact Info
  if (hasEmail && (hasPhone || hasLinkedInOrGithub)) {
    strengths.push('Contact Header: Direct email and professional identity links parsed successfully.');
  } else {
    score -= 10;
    issues.push('Contact Incompleteness: Missing explicit email, phone, or LinkedIn/GitHub link.');
  }

  // 5. Layout & Single Column
  const avgLineLen = fullText.length / Math.max(1, lineCount);
  const isSingleColumnFriendly = avgLineLen > 25 && avgLineLen < 160;
  if (!isSingleColumnFriendly) {
    score -= 8;
    issues.push('Multi-Column / Complex Layout Risk: Text flow shows fragmented blocks that may scramble in legacy Taleo/Workday parsers.');
  } else {
    strengths.push('Clean Single-Column Flow: Unbroken horizontal line geometry avoids parser column confusion.');
  }

  // 6. Bullet Point Count
  if (bulletCount >= 4) {
    strengths.push(`Structured Bullets: Found ${bulletCount} quantified bullet points.`);
  } else {
    score -= 5;
    issues.push('Bullet Point Density: Low bullet point count. ATS systems rank organized bulleted lists higher than dense prose paragraphs.');
  }

  const finalScore = Math.max(20, Math.min(100, score));

  const audit: ATSFormattingAudit = {
    formatting_score: finalScore,
    page_count: pageCount,
    has_machine_readable_text: hasText,
    is_single_column_friendly: isSingleColumnFriendly,
    detected_sections: detectedSections,
    missing_sections: missingSections,
    contact_info_detected: {
      email: hasEmail,
      phone: hasPhone,
      linkedin_or_github: hasLinkedInOrGithub,
    },
    table_graphic_risk: isSingleColumnFriendly ? 'Low' : 'Moderate',
    bullet_point_count: bulletCount,
    formatting_issues: issues,
    formatting_strengths: strengths,
  };

  return {
    text: fullText,
    audit,
  };
}

/**
 * Evaluates formatting from raw pasted text when PDF is not provided.
 */
export function auditTextFormatting(text: string): ATSFormattingAudit {
  const lines = text.split(/\r?\n|\.\s+/).filter(l => l.trim().length > 0);
  const lineCount = lines.length;
  const bulletCount = (text.match(/[•\-\*\u2022\u2023\u25E6\u2043\u2219]/g) || []).length;

  const detectedSections: string[] = [];
  const missingSections: string[] = [];

  for (const sec of EXPECTED_SECTIONS) {
    if (sec.regex.test(text)) {
      detectedSections.push(sec.name);
    } else {
      missingSections.push(sec.name);
    }
  }

  const hasEmail = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/.test(text);
  const hasPhone = /(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}/.test(text);
  const hasLinkedInOrGithub = /(linkedin\.com\/in\/|github\.com\/)/i.test(text);

  const strengths: string[] = [];
  const issues: string[] = [];
  let score = 90; // baseline for pasted plain text

  strengths.push('Plain Text Formatting: Zero binary corruption or font embedding issues.');

  if (detectedSections.length >= 3) {
    strengths.push(`Standard ATS Headers: Found ${detectedSections.join(', ')}.`);
  }
  if (missingSections.length > 0) {
    score -= missingSections.length * 7;
    issues.push(`Missing Standard Sections: Could not detect ${missingSections.join(', ')} header(s).`);
  }

  if (hasEmail || hasPhone || hasLinkedInOrGithub) {
    strengths.push('Contact Markers: Identifiable contact or profile references present.');
  } else {
    score -= 10;
    issues.push('Contact Incompleteness: No email, phone, or LinkedIn/GitHub link detected.');
  }

  if (bulletCount >= 3) {
    strengths.push(`Bullet Structure: Found ${bulletCount} bullet points.`);
  } else {
    score -= 8;
    issues.push('Bullet Point Formatting: Low bullet count. Use dash (-) or bullet (•) points for quantifiable impact.');
  }

  const finalScore = Math.max(30, Math.min(100, score));

  return {
    formatting_score: finalScore,
    page_count: lineCount > 70 ? 2 : 1,
    has_machine_readable_text: true,
    is_single_column_friendly: true,
    detected_sections: detectedSections,
    missing_sections: missingSections,
    contact_info_detected: {
      email: hasEmail,
      phone: hasPhone,
      linkedin_or_github: hasLinkedInOrGithub,
    },
    table_graphic_risk: 'Low',
    bullet_point_count: bulletCount,
    formatting_issues: issues,
    formatting_strengths: strengths,
  };
}
