import os
import json
import argparse
import pymupdf4llm

class PDFContentExtractor:
    """Class to extract Markdown-formatted content from PDF files."""
    
    def __init__(self, output_format: str = "markdown"):
        self.output_format = output_format

    def extract(self, file_path: str) -> str:
        """Converts PDF pages into a single Markdown string."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"No file found at {file_path}")
        
        # pymupdf4llm.to_markdown is the most robust method for LLM-ready text
        if self.output_format == "markdown":
            md_text = pymupdf4llm.to_markdown(file_path)
        elif self.output_format == "json":
            md_text = pymupdf4llm.to_json(file_path)
        else:
            raise ValueError(f"Unsupported format: {self.output_format}")

        return md_text

def main():
    parser = argparse.ArgumentParser(description="PDF Extractor")
    parser.add_argument("--file", type=str, default="sample.pdf", help="Path to PDF")
    args = parser.parse_args()

   # if args.sample:
   #     print("CI Test Mode: PyMuPDF4LLM logic verified.")
   #     return

    try:
        extractor = PDFContentExtractor()
        content = extractor.extract(args.file)
        
        # We output as JSON so it plays nice with your GitHub Actions/Docker logs
        output = {
            "filename": args.file,
            "content_length": len(content),
            "payload": content
        }
        print(json.dumps(output, indent=2))
        
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        exit(1)

if __name__ == "__main__":
    main()