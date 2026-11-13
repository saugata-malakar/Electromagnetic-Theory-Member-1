"""
export_presentation.py
======================
Uses PowerPoint COM automation via win32com to:
1. Export 'EC3104_15_Slide_Capstone_Presentation.pptx' to 'EC3104_15_Slide_Capstone_Presentation.pdf'
2. Export each slide to high-resolution PNG in 'presentation_slide_previews/' for visual inspection.
"""

import os
import sys
import win32com.client

def export():
    workspace = os.path.abspath(os.path.dirname(__file__))
    pptx_path = os.path.join(workspace, "EC3104_15_Slide_Capstone_Presentation.pptx")
    pdf_path = os.path.join(workspace, "EC3104_15_Slide_Capstone_Presentation.pdf")
    previews_dir = os.path.join(workspace, "presentation_slide_previews")
    os.makedirs(previews_dir, exist_ok=True)

    if not os.path.exists(pptx_path):
        print(f"Error: {pptx_path} does not exist.")
        return

    print("Launching PowerPoint application...")
    ppt_app = win32com.client.Dispatch("PowerPoint.Application")
    # Open presentation (ReadOnly, Untitled, WithWindow)
    # WithWindow = 0 (msoFalse) or 1 (msoTrue)
    # 0 = hidden, 1 = visible
    try:
        pres = ppt_app.Presentations.Open(pptx_path, True, False, False)
        print(f"Opened presentation with {len(pres.Slides)} slides.")

        # Export to PDF (ppSaveAsPDF = 32)
        print(f"Exporting to PDF: {pdf_path}...")
        pres.SaveAs(pdf_path, 32)
        print("PDF export complete!")

        # Export each slide to PNG
        print("Exporting slides to PNG previews...")
        for i, slide in enumerate(pres.Slides):
            slide_img_path = os.path.join(previews_dir, f"slide_{i+1:02d}.png")
            slide.Export(slide_img_path, "PNG", 1920, 1080)
            print(f"  Slide {i+1} exported: {slide_img_path}")

        pres.Close()
        print("Export process finished successfully!")
    except Exception as e:
        print(f"Export failed with error: {e}")
    finally:
        try:
            ppt_app.Quit()
        except Exception:
            pass

if __name__ == "__main__":
    export()
