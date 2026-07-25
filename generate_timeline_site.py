import os
import sys
import html as html_lib


def build_gallery_section(script_dir, subfolder, display_name):
    """Scan images/<subfolder>/ and return HTML for the grid, or an empty-state block."""
    folder_rel = "images/" + subfolder
    folder_abs = os.path.join(script_dir, "images", subfolder)
    valid_exts = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

    files = []
    if os.path.isdir(folder_abs):
        files = sorted(
            f for f in os.listdir(folder_abs)
            if os.path.splitext(f.lower())[1] in valid_exts
            and not f.startswith(".")
        )

    if not files:
        return (
            '<div class="gallery-empty">'
            '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24">'
            '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" '
            'd="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14'
            'm-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>'
            '</svg>'
            f'<h3>No {display_name} yet</h3>'
            f'<p>This folder is empty. To contribute:</p>'
            '<ol>'
            f'<li>Add JPG, PNG, GIF, or WEBP files to <code>{folder_rel}/</code></li>'
            '<li>Commit and push to the repo</li>'
            '<li>Re-run <code>python3 generate_timeline_site-v5.py</code></li>'
            '</ol>'
            '</div>'
        )

    items = []
    for f in files:
        stem = os.path.splitext(f)[0]
        label = html_lib.escape(stem.replace("-", " ").replace("_", " ").strip().title())
        safe_name = html_lib.escape(f, quote=True)
        items.append(
            f'<div class="gallery-item">'
            f'<img src="{folder_rel}/{safe_name}" alt="{label}" loading="lazy">'
            f'<div class="gallery-caption">{label}</div>'
            f'</div>'
        )
    return '<div class="gallery-grid">' + "".join(items) + '</div>'


def main():
    try:
        # Determine the output path dynamically (relative to the script's directory for the user)
        script_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in locals() else os.getcwd()
        
        # In a sandbox environment, we can also write to /workspace/scratch/ for testing,
        # but for the user it should write in their current directory.
        if '/workspace' in script_dir:
            output_path = os.path.join('/workspace/scratch', 'index.html')
        else:
            output_path = os.path.join(script_dir, 'index.html')

        html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CJP Protest Timeline - Cockroach Janta Party</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:ital,wght@0,600;0,700;1,400&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary-orange: #FF9933; /* Saffron/Orange - Official CJP Color & Indian Flag */
            --primary-dark-orange: #E67E22;
            --accent-green: #138808;   /* Indian Green */
            --accent-blue: #000080;    /* Navy Blue (Ashoka Chakra) */
            --accent-light-blue: #E8F0FE;
            --bg-white: #FFFFFF;
            --bg-light: #F8FAFC;       /* Clean Off-white */
            --text-dark: #0F172A;      /* Slate 900 */
            --text-muted: #64748B;     /* Slate 500 */
            --border-color: #E2E8F0;   /* Slate 200 */
            --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -2px rgba(0, 0, 0, 0.04);
            --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            --font-serif: 'Playfair Display', Georgia, serif;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            scroll-behavior: smooth;
        }

        body {
            font-family: var(--font-sans);
            background-color: var(--bg-light);
            color: var(--text-dark);
            line-height: 1.6;
            overflow-x: hidden;
        }

        /* Patriotic Header Badge & Flag Bar */
        .flag-bar {
            height: 6px;
            width: 100%;
            display: flex;
        }
        .flag-orange { background-color: var(--primary-orange); flex: 1; }
        .flag-white { background-color: #FFFFFF; flex: 1; }
        .flag-green { background-color: var(--accent-green); flex: 1; }

        header {
            background-color: var(--bg-white);
            border-bottom: 1px solid var(--border-color);
            position: sticky;
            top: 0;
            z-index: 100;
            padding: 1.25rem 2rem;
            box-shadow: var(--shadow);
        }

        .header-container {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo-section {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .logo-badge {
            background: linear-gradient(135deg, var(--primary-orange), var(--accent-green));
            color: white;
            font-weight: 800;
            font-size: 1.25rem;
            width: 44px;
            height: 44px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 2px solid var(--accent-blue);
            box-shadow: 0 3px 6px rgba(0,0,0,0.1);
        }

        .logo-title h1 {
            font-size: 1.35rem;
            font-weight: 800;
            letter-spacing: -0.5px;
            color: var(--accent-blue);
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .logo-title p {
            font-size: 0.75rem;
            color: var(--text-muted);
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 1.5px;
        }

        /* Navigation Tabs */
        .nav-tabs {
            display: flex;
            background-color: var(--bg-light);
            border: 1px solid var(--border-color);
            padding: 5px;
            border-radius: 30px;
            gap: 4px;
        }

        .tab-btn {
            background: none;
            border: none;
            padding: 0.65rem 1.4rem;
            font-family: var(--font-sans);
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text-muted);
            cursor: pointer;
            border-radius: 25px;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .tab-btn:hover {
            color: var(--accent-blue);
        }

        .tab-btn.active {
            background-color: var(--bg-white);
            color: var(--accent-blue);
            box-shadow: var(--shadow);
            border: 1px solid rgba(0,0,80,0.08);
        }

        /* Main Screen Layout (Classic Split Screen) */
        main {
            max-width: 1500px;
            margin: 0 auto;
            padding: 2rem;
            min-height: calc(100vh - 100px);
        }

        .view-panel {
            display: none;
        }

        .view-panel.active {
            display: block;
        }

        /* Split-Screen Interactive Timeline */
        .split-container {
            display: flex;
            gap: 2.5rem;
            height: calc(100vh - 180px);
            min-height: 650px;
        }

        /* Left Side: Succinct Timeline (Scrollable & Clean) */
        .timeline-column {
            flex: 0 0 40%;
            background-color: var(--bg-white);
            border-radius: 16px;
            border: 1px solid var(--border-color);
            padding: 2rem 1.5rem;
            overflow-y: auto;
            position: relative;
            box-shadow: var(--shadow);
        }

        .timeline-column::-webkit-scrollbar {
            width: 6px;
        }
        .timeline-column::-webkit-scrollbar-track {
            background: transparent;
        }
        .timeline-column::-webkit-scrollbar-thumb {
            background-color: var(--border-color);
            border-radius: 10px;
        }

        .column-title {
            font-size: 1.15rem;
            font-weight: 700;
            color: var(--accent-blue);
            margin-bottom: 2rem;
            padding-bottom: 0.75rem;
            border-bottom: 2px solid var(--primary-orange);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .column-title span {
            background-color: var(--accent-light-blue);
            color: var(--accent-blue);
            font-size: 0.75rem;
            padding: 4px 10px;
            border-radius: 12px;
            font-weight: 600;
        }

        /* The Vertical Line */
        .timeline-axis {
            position: relative;
            padding-left: 2rem;
        }

        .timeline-axis::before {
            content: '';
            position: absolute;
            left: 7px;
            top: 10px;
            bottom: 10px;
            width: 3px;
            background: linear-gradient(to bottom, var(--primary-orange) 0%, var(--accent-green) 100%);
            border-radius: 3px;
        }

        /* Timeline Items - Succinct list */
        .timeline-item-btn {
            width: 100%;
            text-align: left;
            background: none;
            border: none;
            padding: 1.2rem 1rem;
            margin-bottom: 1rem;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.25s ease;
            position: relative;
            display: block;
            border: 1px solid transparent;
        }

        .timeline-item-btn:hover {
            background-color: var(--bg-light);
            transform: translateX(4px);
        }

        .timeline-item-btn.active {
            background-color: #FFF9F3; /* Light orange tint */
            border-color: rgba(255, 153, 51, 0.4);
            box-shadow: var(--shadow);
        }

        /* Glow Dot on Timeline Line */
        .timeline-item-btn::before {
            content: '';
            position: absolute;
            left: -2.35rem;
            top: 50%;
            transform: translateY(-50%);
            width: 13px;
            height: 13px;
            border-radius: 50%;
            background-color: var(--bg-white);
            border: 3px solid var(--primary-orange);
            transition: all 0.3s ease;
            z-index: 2;
        }

        .timeline-item-btn.active::before {
            background-color: var(--primary-orange);
            border-color: var(--accent-blue);
            box-shadow: 0 0 10px var(--primary-orange);
            transform: translateY(-50%) scale(1.3);
        }

        .btn-date {
            font-size: 0.8rem;
            font-weight: 700;
            color: var(--primary-orange);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 0.35rem;
            display: inline-block;
        }

        .timeline-item-btn.active .btn-date {
            color: var(--primary-dark-orange);
        }

        .btn-title {
            font-size: 0.95rem;
            font-weight: 600;
            color: var(--text-dark);
            line-height: 1.35;
        }

        .timeline-item-btn.active .btn-title {
            color: var(--accent-blue);
        }

        /* Right Side: Detailed Narrative Display */
        .detail-column {
            flex: 0 0 60%;
            background-color: var(--bg-white);
            border-radius: 16px;
            border: 1px solid var(--border-color);
            padding: 2.5rem;
            overflow-y: auto;
            box-shadow: var(--shadow-lg);
            display: flex;
            flex-direction: column;
        }

        .detail-column::-webkit-scrollbar {
            width: 6px;
        }
        .detail-column::-webkit-scrollbar-track {
            background: transparent;
        }
        .detail-column::-webkit-scrollbar-thumb {
            background-color: var(--border-color);
            border-radius: 10px;
        }

        /* Default Empty State */
        .empty-detail-state {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            height: 100%;
            color: var(--text-muted);
            padding: 4rem;
        }

        .empty-detail-state svg {
            width: 80px;
            height: 80px;
            color: var(--primary-orange);
            margin-bottom: 1.5rem;
            stroke-width: 1.5;
            animation: bounce 2s infinite;
        }

        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }

        /* Rich Detail Structure */
        .detail-content {
            display: none;
            animation: fadeIn 0.4s ease forwards;
        }

        .detail-content.active {
            display: block;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(15px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .detail-header {
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 1.5rem;
            margin-bottom: 2rem;
        }

        .detail-tag {
            display: inline-block;
            background-color: #FFF3E0;
            color: var(--primary-dark-orange);
            font-size: 0.75rem;
            font-weight: 700;
            padding: 5px 12px;
            border-radius: 20px;
            text-transform: uppercase;
            letter-spacing: 1px;
            border: 1px solid rgba(255,153,51,0.25);
            margin-bottom: 0.75rem;
        }

        .detail-tag.success-tag {
            background-color: #E8F5E9;
            color: var(--accent-green);
            border-color: rgba(19,136,8,0.2);
        }

        .detail-tag.blue-tag {
            background-color: var(--accent-light-blue);
            color: var(--accent-blue);
            border-color: rgba(0,0,128,0.2);
        }

        .detail-date {
            font-family: var(--font-serif);
            font-size: 1.15rem;
            font-weight: 600;
            color: var(--text-muted);
            margin-bottom: 0.5rem;
        }

        .detail-title {
            font-family: var(--font-serif);
            font-size: 2.25rem;
            color: var(--accent-blue);
            line-height: 1.2;
            font-weight: 800;
        }

        .detail-body {
            font-size: 1.05rem;
            color: #334155;
            line-height: 1.75;
        }

        .detail-body p {
            margin-bottom: 1.5rem;
        }

        .detail-body strong {
            color: var(--accent-blue);
        }

        /* Styled Quote blocks */
        .blue-quote-box {
            background: linear-gradient(to right, #F0FDF4, #ECFDF5);
            border-left: 5px solid var(--accent-green);
            padding: 1.5rem;
            border-radius: 0 12px 12px 0;
            margin: 2rem 0;
            font-style: italic;
            box-shadow: var(--shadow);
            border: 1px solid var(--border-color);
            border-left: 5px solid var(--accent-blue);
        }

        .blue-quote-box.ink-attack {
            background: linear-gradient(to right, #EFF6FF, #F8FAFC);
            border-left: 5px solid var(--accent-blue);
        }

        .quote-author {
            font-style: normal;
            font-weight: 700;
            color: var(--accent-blue);
            font-size: 0.95rem;
            margin-top: 0.75rem;
            display: block;
            text-align: right;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        /* Unified Visual Media & Mockups */
        .media-container {
            margin: 2rem 0;
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid var(--border-color);
            box-shadow: var(--shadow);
            background-color: var(--bg-light);
            position: relative;
        }

        .media-image-placeholder {
            width: 100%;
            height: 320px;
            object-fit: contain;
            display: block;
            background-color: var(--bg-light);
        }

        .media-caption {
            background-color: var(--bg-white);
            padding: 1rem 1.25rem;
            font-size: 0.85rem;
            color: var(--text-muted);
            border-top: 1px solid var(--border-color);
            font-weight: 500;
        }

        .media-caption strong {
            color: var(--text-dark);
        }

        /* Simulated X/Twitter Post Styles */
        .tweet-card {
            background-color: var(--bg-white);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 1.5rem;
            margin: 2rem 0;
            box-shadow: var(--shadow);
            font-family: var(--font-sans);
        }

        .tweet-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1rem;
        }

        .tweet-profile {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .tweet-avatar {
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background-color: #E2E8F0;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            color: white;
            font-size: 1.2rem;
            border: 1px solid var(--border-color);
        }

        .tweet-user-info {
            display: flex;
            flex-direction: column;
        }

        .tweet-name {
            font-weight: 700;
            color: var(--text-dark);
            font-size: 0.95rem;
            display: flex;
            align-items: center;
            gap: 4px;
        }

        .tweet-verified-badge {
            color: #1DA1F2;
            width: 16px;
            height: 16px;
        }

        .tweet-handle {
            color: var(--text-muted);
            font-size: 0.85rem;
        }

        .tweet-logo {
            color: var(--text-dark);
            font-weight: 800;
            font-size: 1.25rem;
        }

        .tweet-content {
            font-size: 1.15rem;
            color: var(--text-dark);
            line-height: 1.5;
            margin-bottom: 1rem;
        }

        .tweet-hashtags {
            color: #1DA1F2;
            cursor: pointer;
        }

        .tweet-footer {
            border-top: 1px solid var(--border-color);
            padding-top: 0.75rem;
            display: flex;
            gap: 1.5rem;
            color: var(--text-muted);
            font-size: 0.8rem;
            font-weight: 600;
        }

        .tweet-stat span {
            color: var(--text-dark);
            font-weight: 700;
        }

        /* Custom Audio/Video Mockup Card for Rakhi Sawant */
        .video-player-container {
            background-color: #0B0F19; /* Sleek Dark Media Player background */
            border-radius: 14px;
            padding: 2.5rem 2rem;
            margin: 2rem 0;
            position: relative;
            color: white;
            box-shadow: var(--shadow-lg);
            border: 2px solid var(--primary-orange);
        }

        .video-player-overlay {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            z-index: 2;
        }

        .video-icon {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background-color: rgba(255, 153, 51, 0.2);
            border: 2px solid var(--primary-orange);
            color: var(--primary-orange);
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 1rem;
            animation: pulse-ring 2s infinite;
        }

        @keyframes pulse-ring {
            0% { box-shadow: 0 0 0 0 rgba(255, 153, 51, 0.4); }
            70% { box-shadow: 0 0 0 15px rgba(255, 153, 51, 0); }
            100% { box-shadow: 0 0 0 0 rgba(255, 153, 51, 0); }
        }

        .video-player-title {
            font-weight: 700;
            font-size: 1.1rem;
            margin-bottom: 0.5rem;
            color: #FFF;
        }

        .video-player-subtitle {
            font-size: 0.8rem;
            color: var(--primary-orange);
            text-transform: uppercase;
            letter-spacing: 1.5px;
            font-weight: 700;
            margin-bottom: 1.5rem;
        }

        .audio-wave-graphic {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 4px;
            height: 40px;
            margin-bottom: 1.5rem;
            width: 100%;
        }

        .audio-wave-bar {
            width: 3px;
            height: 15px;
            background-color: var(--primary-orange);
            border-radius: 3px;
            animation: audio-pulse 1.2s infinite ease-in-out;
        }

        .audio-wave-bar:nth-child(even) {
            background-color: var(--accent-green);
            animation-delay: 0.2s;
            height: 30px;
        }

        .audio-wave-bar:nth-child(3n) {
            background-color: #FFF;
            animation-delay: 0.4s;
            height: 40px;
        }

        @keyframes audio-pulse {
            0%, 100% { transform: scaleY(1); }
            50% { transform: scaleY(2); }
        }

        .transcript-container {
            background-color: rgba(255,255,255,0.06);
            border-radius: 8px;
            padding: 1rem;
            font-size: 0.9rem;
            text-align: left;
            line-height: 1.6;
            font-style: italic;
            border-left: 3px solid var(--primary-orange);
        }

        /* "Watch on Instagram" link inside the video mockup */
        .video-watch-link {
            display: inline-flex;
            align-items: center;
            margin-top: 1.5rem;
            padding: 0.65rem 1.4rem;
            background: linear-gradient(135deg, #833AB4 0%, #E1306C 50%, #F77737 100%);
            color: #FFF;
            border-radius: 24px;
            font-size: 0.85rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            text-decoration: none;
            box-shadow: 0 4px 12px rgba(225, 48, 108, 0.35);
            transition: all 0.25s ease;
        }

        .video-watch-link:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 18px rgba(225, 48, 108, 0.5);
        }

        .video-watch-link:active {
            transform: translateY(0);
        }

        /* View Panel: Heroes Grid */
        .heroes-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 2rem;
            margin-top: 1.5rem;
        }

        .hero-card {
            background-color: var(--bg-white);
            border-radius: 16px;
            border: 1px solid var(--border-color);
            padding: 2.25rem;
            box-shadow: var(--shadow);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .hero-card:hover {
            transform: translateY(-6px);
            box-shadow: var(--shadow-lg);
            border-color: rgba(0,0,128,0.15);
        }

        .hero-badge {
            position: absolute;
            top: 20px;
            right: 20px;
            background-color: var(--accent-light-blue);
            color: var(--accent-blue);
            font-size: 0.7rem;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .hero-number {
            font-size: 3rem;
            font-weight: 900;
            color: rgba(0,0,128,0.05);
            line-height: 1;
            margin-bottom: 0.5rem;
        }

        .hero-name {
            font-family: var(--font-serif);
            font-size: 1.65rem;
            color: var(--accent-blue);
            font-weight: 800;
            margin-bottom: 0.25rem;
        }

        .hero-outlet {
            font-weight: 600;
            color: var(--primary-orange);
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 1.25rem;
        }

        .hero-bio {
            color: #475569;
            font-size: 0.95rem;
            line-height: 1.65;
            margin-bottom: 1.5rem;
        }

        .hero-quote {
            background-color: var(--bg-light);
            border-left: 3px solid var(--accent-green);
            padding: 1rem;
            border-radius: 0 8px 8px 0;
            font-size: 0.85rem;
            font-style: italic;
            color: var(--text-dark);
        }

        /* View Panel: Context & Memorial */
        .context-section {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 2.5rem;
            margin-bottom: 3rem;
        }

        @media (max-width: 900px) {
            .context-section {
                grid-template-columns: 1fr;
            }
        }

        .context-card {
            background-color: var(--bg-white);
            border-radius: 16px;
            border: 1px solid var(--border-color);
            padding: 2.5rem;
            box-shadow: var(--shadow);
        }

        .context-card-title {
            font-family: var(--font-serif);
            font-size: 1.8rem;
            color: var(--accent-blue);
            margin-bottom: 1.25rem;
            font-weight: 800;
            display: flex;
            align-items: center;
            gap: 12px;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 1rem;
        }

        .context-card-title svg {
            color: var(--primary-orange);
            width: 28px;
            height: 28px;
        }

        .context-card-body {
            font-size: 1rem;
            color: #475569;
            line-height: 1.7;
        }

        .context-card-body p {
            margin-bottom: 1.25rem;
        }

        /* 21 Candles Memorial */
        .memorial-container {
            background: radial-gradient(circle at center, #111424, #070913); /* Solemn night background */
            border-radius: 20px;
            padding: 3rem;
            color: white;
            box-shadow: var(--shadow-lg);
            margin-top: 1rem;
            border: 2px solid var(--primary-orange);
        }

        .memorial-header {
            text-align: center;
            max-width: 800px;
            margin: 0 auto 3rem auto;
        }

        .memorial-title {
            font-family: var(--font-serif);
            font-size: 2.25rem;
            color: var(--primary-orange);
            font-weight: 800;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
        }

        .memorial-title span {
            color: white;
        }

        .memorial-subtitle {
            font-size: 0.95rem;
            color: #94A3B8;
            line-height: 1.6;
        }

        .candles-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(90px, 1fr));
            gap: 1.5rem;
            justify-items: center;
        }

        /* 3D Pure CSS Flickering Candle */
        .candle-wrapper {
            display: flex;
            flex-direction: column;
            align-items: center;
            cursor: pointer;
            position: relative;
            transition: transform 0.2s ease;
        }

        .candle-wrapper:hover {
            transform: scale(1.15);
        }

        .candle-flame {
            width: 14px;
            height: 28px;
            background: linear-gradient(to top, rgba(255, 100, 0, 0) 0%, rgba(255, 153, 51, 1) 40%, rgba(255, 230, 100, 1) 100%);
            border-radius: 50% 50% 20% 20%;
            box-shadow: 0 0 15px rgba(255, 153, 51, 0.8), 0 0 30px rgba(255, 100, 0, 0.5);
            animation: flicker 1s infinite alternate;
            transform-origin: center bottom;
        }

        .candle-wick {
            width: 2px;
            height: 6px;
            background-color: #334155;
        }

        .candle-body {
            width: 18px;
            height: 44px;
            background: linear-gradient(to right, #FFF 0%, #E2E8F0 50%, #CBD5E1 100%);
            border-radius: 3px 3px 2px 2px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.4);
            position: relative;
            overflow: hidden;
        }

        /* Small Indian flag dynamic overlay strip on candles */
        .candle-body::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 6px;
            background: linear-gradient(to right, var(--primary-orange), #FFF, var(--accent-green));
        }

        .candle-label {
            margin-top: 0.5rem;
            font-size: 0.65rem;
            color: #94A3B8;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .candle-wrapper:hover .candle-label {
            color: var(--primary-orange);
        }

        /* Flickering Animation */
        @keyframes flicker {
            0% { transform: scale(1) rotate(-1deg); }
            20% { transform: scale(1.1) rotate(1deg) skewX(2deg); }
            40% { transform: scale(0.9) rotate(-2deg); }
            60% { transform: scale(1.05) rotate(2deg) skewX(-1deg); }
            80% { transform: scale(0.95) rotate(-1deg); }
            100% { transform: scale(1.15) rotate(0deg) skewX(1deg); }
        }

        /* CSS Candle Tooltip style */
        .candle-wrapper .tooltip {
            visibility: hidden;
            width: 200px;
            background-color: #1E293B;
            color: #fff;
            text-align: center;
            border-radius: 6px;
            padding: 8px 12px;
            position: absolute;
            z-index: 10;
            bottom: 125%;
            left: 50%;
            margin-left: -100px;
            opacity: 0;
            transition: opacity 0.3s;
            font-size: 0.75rem;
            line-height: 1.4;
            border: 1px solid rgba(255, 153, 51, 0.4);
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.5);
        }

        .candle-wrapper:hover .tooltip {
            visibility: visible;
            opacity: 1;
        }

        /* Responsive Mobile Layouts */
        /* View Panel: Gallery (sub-tabs + image grid) */
        .gallery-header {
            text-align: center;
        }

        .gallery-subtabs {
            display: inline-flex;
            background-color: var(--bg-white);
            border: 1px solid var(--border-color);
            padding: 5px;
            border-radius: 30px;
            gap: 4px;
            margin: 2rem auto 2.5rem;
            box-shadow: var(--shadow);
        }

        .sub-tab-btn {
            background: none;
            border: none;
            padding: 0.7rem 1.6rem;
            font-family: var(--font-sans);
            font-size: 0.9rem;
            font-weight: 600;
            color: var(--text-muted);
            cursor: pointer;
            border-radius: 25px;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }

        .sub-tab-btn:hover {
            color: var(--accent-blue);
        }

        .sub-tab-btn.active {
            background: linear-gradient(135deg, var(--primary-orange), var(--primary-dark-orange));
            color: white;
            box-shadow: 0 3px 8px rgba(255, 153, 51, 0.35);
        }

        .gallery-subpanel {
            display: none;
            animation: fadeIn 0.4s ease forwards;
        }

        .gallery-subpanel.active {
            display: block;
        }

        .gallery-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 1.5rem;
            margin-top: 1rem;
        }

        .gallery-item {
            background-color: var(--bg-white);
            border-radius: 14px;
            overflow: hidden;
            border: 1px solid var(--border-color);
            box-shadow: var(--shadow);
            transition: all 0.25s ease;
        }

        .gallery-item:hover {
            transform: translateY(-4px);
            box-shadow: var(--shadow-lg);
            border-color: rgba(255, 153, 51, 0.4);
        }

        .gallery-item img {
            width: 100%;
            height: 240px;
            object-fit: cover;
            display: block;
            background-color: var(--bg-light);
        }

        .gallery-caption {
            padding: 1rem 1.15rem;
            font-size: 0.9rem;
            color: var(--text-dark);
            font-weight: 500;
            border-top: 1px solid var(--border-color);
        }

        .gallery-empty {
            text-align: center;
            padding: 4rem 2rem;
            background-color: var(--bg-white);
            border-radius: 16px;
            border: 2px dashed var(--border-color);
            color: var(--text-muted);
            max-width: 640px;
            margin: 0 auto;
        }

        .gallery-empty svg {
            width: 64px;
            height: 64px;
            color: var(--primary-orange);
            margin-bottom: 1.25rem;
            stroke-width: 1.5;
        }

        .gallery-empty h3 {
            font-family: var(--font-serif);
            font-size: 1.4rem;
            color: var(--accent-blue);
            margin-bottom: 0.75rem;
        }

        .gallery-empty p {
            font-size: 0.95rem;
            line-height: 1.6;
        }

        .gallery-empty code {
            background-color: var(--bg-light);
            color: var(--primary-dark-orange);
            padding: 3px 8px;
            border-radius: 6px;
            font-family: 'Courier New', monospace;
            font-size: 0.85rem;
            border: 1px solid var(--border-color);
        }

        .gallery-empty ol {
            text-align: left;
            max-width: 380px;
            margin: 1.5rem auto 0;
            padding-left: 1.25rem;
            font-size: 0.9rem;
            line-height: 1.85;
        }

        @media (max-width: 1024px) {
            .split-container {
                flex-direction: column;
                height: auto;
            }

            .timeline-column {
                flex: none;
                width: 100%;
                height: 400px;
            }

            .detail-column {
                flex: none;
                width: 100%;
                height: auto;
                min-height: 400px;
            }
        }

        @media (max-width: 768px) {
            header {
                padding: 1rem;
            }
            .header-container {
                flex-direction: column;
                gap: 1rem;
            }
            main {
                padding: 1rem;
            }
            .detail-title {
                font-size: 1.75rem;
            }
        }
    </style>
</head>
<body>

    <!-- Tri-Color Bar Representing Indian National Flag -->
    <div class="flag-bar">
        <div class="flag-orange"></div>
        <div class="flag-white"></div>
        <div class="flag-green"></div>
    </div>

    <!-- Header & Navigation -->
    <header>
        <div class="header-container">
            <div class="logo-section">
                <div class="logo-badge">&#128030;</div>
                <div class="logo-title">
                    <h1>CJP <span>PROTESTS</span></h1>
                    <p>Cockroach Janta Party Archive</p>
                </div>
            </div>

            <nav class="nav-tabs">
                <button class="tab-btn active" onclick="switchTab('timeline')">
                    <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                    Interactive Timeline
                </button>
                <button class="tab-btn" onclick="switchTab('heroes')">
                    <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z"/></svg>
                    Heroes of the Ground
                </button>
                <button class="tab-btn" onclick="switchTab('gallery')">
                    <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
                    Gallery
                </button>
                <button class="tab-btn" onclick="switchTab('context')">
                    <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.907c.961 0 1.36 1.253.588 1.81l-3.974 2.89a1 1 0 00-.364 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.89a1 1 0 00-1.176 0l-3.976 2.89c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.364-1.118L2.05 12.002c-.773-.557-.375-1.81.587-1.81H7.53a1 1 0 00.95-.69l1.519-4.674z"/></svg>
                    Memorial & Context
                </button>
            </nav>
        </div>
    </header>

    <main>
        
        <!-- SECTION 1: TIMELINE PANEL (CLASSIC SPLIT SCREEN) -->
        <div id="timeline-panel" class="view-panel active">
            <div class="split-container">
                
                <!-- Left Column: Succinct Navigation Axis -->
                <div class="timeline-column">
                    <div class="column-title">
                        <span>Milestones</span>
                        <span>Click to read details</span>
                    </div>

                    <div class="timeline-axis">
                        <!-- May 15 -->
                        <button class="timeline-item-btn active" onclick="showDetail('day1')">
                            <span class="btn-date">May 15, 2026</span>
                            <div class="btn-title">The "Cockroach" Remark Spark</div>
                        </button>

                        <!-- May 16 -->
                        <button class="timeline-item-btn" onclick="showDetail('day2')">
                            <span class="btn-date">May 16, 2026</span>
                            <div class="btn-title">Birth of Cockroach Janta Party</div>
                        </button>

                        <!-- May 21 -->
                        <button class="timeline-item-btn" onclick="showDetail('day3')">
                            <span class="btn-date">May 21, 2026</span>
                            <div class="btn-title">X Account Blocked Under Section 69A</div>
                        </button>

                        <!-- May 22 -->
                        <button class="timeline-item-btn" onclick="showDetail('day4')">
                            <span class="btn-date">May 22, 2026</span>
                            <div class="btn-title">Celebrity Backlash & Streisand Effect</div>
                        </button>

                        <!-- June 6 -->
                        <button class="timeline-item-btn" onclick="showDetail('day5')">
                            <span class="btn-date">June 06, 2026</span>
                            <div class="btn-title">NEET Paper Leak Scandal Escalates</div>
                        </button>

                        <!-- July 11 -->
                        <button class="timeline-item-btn" onclick="showDetail('day6')">
                            <span class="btn-date">July 11, 2026</span>
                            <div class="btn-title">Delhi HC Restores CJP's X Account</div>
                        </button>

                        <!-- July 18 -->
                        <button class="timeline-item-btn" onclick="showDetail('day7')">
                            <span class="btn-date">July 18, 2026</span>
                            <div class="btn-title">Hunger Strikes & Blue Ink Attack</div>
                        </button>

                        <!-- July 20 -->
                        <button class="timeline-item-btn" onclick="showDetail('day8')">
                            <span class="btn-date">July 20, 2026</span>
                            <div class="btn-title">"Chalo Sansad" March & Clashes</div>
                        </button>

                        <!-- July 21 -->
                        <button class="timeline-item-btn" onclick="showDetail('day9')">
                            <span class="btn-date">July 21, 2026</span>
                            <div class="btn-title">Defiant Campout at Jantar Mantar</div>
                        </button>

                        <!-- July 22 (police lathis) -->
                        <button class="timeline-item-btn" onclick="showDetail('day10')">
                            <span class="btn-date">July 22, 2026</span>
                            <div class="btn-title">Lathis at the Jantar Mantar Campsite</div>
                        </button>

                        <!-- July 22 (Rakhi Sawant video) -->
                        <button class="timeline-item-btn" onclick="showDetail('day11')">
                            <span class="btn-date">July 22, 2026</span>
                            <div class="btn-title">Rakhi Sawant's Viral Video Reaction</div>
                        </button>

                        <!-- July 23 -->
                        <button class="timeline-item-btn" onclick="showDetail('day12')">
                            <span class="btn-date">July 23, 2026</span>
                            <div class="btn-title">PM Offers Deal; CJP Rejects</div>
                        </button>

                        <!-- July 25 -->
                        <button class="timeline-item-btn" onclick="showDetail('day13')">
                            <span class="btn-date">July 25, 2026</span>
                            <div class="btn-title">Cabinet Minister Resigns (Victory!)</div>
                        </button>
                    </div>
                </div>

                <!-- Right Column: Detailed Narrative (Interactive) -->
                <div class="detail-column" id="timeline-detail-box">
                    
                    <!-- INITIAL STATE -->
                    <div id="empty-state" class="empty-detail-state" style="display: none;">
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122"/></svg>
                        <h2 style="font-family: var(--font-serif); font-size: 1.5rem; color: var(--accent-blue); margin-bottom: 0.5rem;">Select a Timeline Milestone</h2>
                        <p>Click on any date dot or title on the left panel to browse detailed event logs, actual celebrity tweets, photo mockups, and historic quotes.</p>
                    </div>

                    <!-- DAY 1 DETAIL -->
                    <div id="day1" class="detail-content active">
                        <div class="detail-header">
                            <span class="detail-tag">The Spark</span>
                            <div class="detail-date">May 15, 2026</div>
                            <h2 class="detail-title">"Cockroaches" of the System</h2>
                        </div>
                        <div class="detail-body">
                            <p>During a high-stakes Supreme Court hearing on student activism and public accountability, Chief Justice of India <strong>Surya Kant</strong> made remarks that compared unemployed youth to <strong>"cockroaches"</strong> and <strong>"parasites of society."</strong> He mentioned that they had no jobs, obtained fake degrees, and spent their time attacking public systems via RTI filings and social media.</p>
                            
                            <div class="blue-quote-box">
                                "There are already parasites who attack the system... There are youngsters like cockroaches who do not get any employment... some of them become media, some become social media, some RTI activists and they start attacking everyone..."
                                <span class="quote-author">CJI Surya Kant (Supreme Court Hearing)</span>
                            </div>

                            <p>Though the Chief Justice later clarified that his comments were aimed specifically at individuals using fraudulent certificates and did not target India's hardworking youth, the quote went viral instantly. A wave of outrage, disbelief, and deep offense swept through social media, setting the stage for an explosive, satirical retaliation from Gen Z.</p>

                            <div class="media-container">
                                <img src="images/cji_sc.jpg" alt="Supreme Court of India" class="media-image-placeholder">
                                <div class="media-caption">
                                    <strong>Figure 1:</strong> Chief Justice of India, Surya Kant and The Supreme Court of India in New Delhi, where the historic "cockroach" remarks were made on May 15.
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- DAY 2 DETAIL -->
                    <div id="day2" class="detail-content">
                        <div class="detail-header">
                            <span class="detail-tag">The Launch</span>
                            <div class="detail-date">May 16, 2026</div>
                            <h2 class="detail-title">The Birth of Cockroach Janta Party (CJP)</h2>
                        </div>
                        <div class="detail-body">
                            <p>Instead of launching traditional protests, 30-year-old political strategist and former Boston University student <strong>Abhijeet Dipke</strong> chose the weapon of absolute satire. Within 24 hours of the judge's remarks, he officially founded the <strong>Cockroach Janta Party (CJP)</strong>, declaring it the "voice of the lazy, unemployed, and resilient youth of India."</p>
                            
                            <p>The movement adopted the cockroach as its mascot—symbolizing an organism that can survive a nuclear blast, just as India's youth are expected to survive systemic neglect and rising unemployment. The party coined the hilarious slogan <strong>"Secular, Socialist, Democratic, Lazy"</strong> and registered maroon as its official political color.</p>

                            <p>CJP released a satirical 5-point manifesto, demanding:
                                <ul style="margin-left: 2rem; margin-bottom: 1.5rem;">
                                    <li>No post-retirement Rajya Sabha seats or government roles for Chief Justices.</li>
                                    <li>50% reservation for women in all legislative and political decision-making roles.</li>
                                    <li>Strict actions and licenses revoked for heavily biased media channels.</li>
                                    <li>Direct, unfiltered, and honest dialogue between the state and unemployed graduates.</li>
                                </ul>
                            </p>

                            <div class="media-container">
                                <img src="images/cjp.jpg" alt="Satirical Youth Party CJP Logo" class="media-image-placeholder">
                                <div class="media-caption">
                                    <strong>Figure 2:</strong> Parody campaign banners and social media templates carrying the "Resilient Cockroach" logo that went viral overnight.
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- DAY 3 DETAIL: CENSORSHIP -->
                    <div id="day3" class="detail-content">
                        <div class="detail-header">
                            <span class="detail-tag blue-tag">Censorship</span>
                            <div class="detail-date">May 21, 2026</div>
                            <h2 class="detail-title">X Account Blocked Under Section 69A</h2>
                        </div>
                        <div class="detail-body">
                            <p>Wary of the movement's rapid viral traction, the Union Government responded aggressively. The Ministry of Electronics and Information Technology (<strong>MeitY</strong>) directed X (formerly Twitter) to block CJP's official handle <code>@CJP_2029</code> in India, citing "national security concerns."</p>

                            <p>The confidential directive, issued under <strong>Section 69A of the IT Act</strong>, was initiated by the Intelligence Bureau (IB), which alleged that the satirical account was posting "inflammatory content" that threatened public order and sovereignty. At the same time, Dipke reported a coordinated digital crackdown: the party's Instagram account was temporarily locked, and access to several other digital assets was restricted.</p>

                            <p>Within hours, the CJP responded with a defiant backup account, <code>@Cockroachisback</code>, carrying the pinned message: <em>"You thought you can get rid of us? Lol."</em></p>
                        </div>
                    </div>

                    <!-- DAY 4 DETAIL: STREISAND EFFECT -->
                    <div id="day4" class="detail-content">
                        <div class="detail-header">
                            <span class="detail-tag">Streisand Effect</span>
                            <div class="detail-date">May 22, 2026</div>
                            <h2 class="detail-title">Celebrity Backlash & Global Explosion</h2>
                        </div>
                        <div class="detail-body">
                            <p>The censorship backfired catastrophically. In a textbook case of the <strong>Streisand Effect</strong>, the attempt to silence CJP triggered a global surge of attention. Within 24 hours, the party's Instagram followers exploded past <strong>16.4 million</strong>, eclipsing the official Instagram account of India's ruling Bharatiya Janata Party (BJP).</p>

                            <p>Across social platforms, prominent celebrities publicly condemned the government's heavy-handed response:</p>

                            <!-- VIR DAS TWEET CARD -->
                            <div class="tweet-card">
                                <div class="tweet-header">
                                    <div class="tweet-profile">
                                        <div class="tweet-avatar" style="background-color: #3B82F6;">VD</div>
                                        <div class="tweet-user-info">
                                            <span class="tweet-name">Vir Das <svg class="tweet-verified-badge" fill="currentColor" viewBox="0 0 24 24"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg></span>
                                            <span class="tweet-handle">@thevirdas</span>
                                        </div>
                                    </div>
                                    <span class="tweet-logo">𝕏</span>
                                </div>
                                <div class="tweet-content">
                                    Why is Cockroach Janata Party withheld in India? It's giving full Streisand effect. <span class="tweet-hashtags">#CockroachJantaParty</span> <span class="tweet-hashtags">#FreeSpeech</span>
                                </div>
                                <div class="tweet-footer">
                                    <span>May 22, 2026</span>
                                    <div class="tweet-stat"><span>74K</span> Retweets</div>
                                    <div class="tweet-stat"><span>320K</span> Likes</div>
                                </div>
                            </div>

                            <!-- CHINMAYI TWEET CARD -->
                            <div class="tweet-card">
                                <div class="tweet-header">
                                    <div class="tweet-profile">
                                        <div class="tweet-avatar" style="background-color: #EC4899;">CS</div>
                                        <div class="tweet-user-info">
                                            <span class="tweet-name">Chinmayi Sripaada <svg class="tweet-verified-badge" fill="currentColor" viewBox="0 0 24 24"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg></span>
                                            <span class="tweet-handle">@chinmayi</span>
                                        </div>
                                    </div>
                                    <span class="tweet-logo">𝕏</span>
                                </div>
                                <div class="tweet-content">
                                    Why is Cockroach Janata Party withheld in India? Blocking a parody page is the ultimate proof of how fragile our systems have become.
                                </div>
                                <div class="tweet-footer">
                                    <span>May 22, 2026</span>
                                    <div class="tweet-stat"><span>45K</span> Retweets</div>
                                    <div class="tweet-stat"><span>180K</span> Likes</div>
                                </div>
                            </div>

                            <p>Major cultural figures publicly stepped in to validate CJP as a legitimate voice, including filmmaker <strong>Anurag Kashyap</strong>, actresses <strong>Sonakshi Sinha</strong>, <strong>Konkona Sen Sharma</strong>, and <strong>Dia Mirza</strong>, internet personality <strong>Uorfi Javed</strong>, and stand-up comedian <strong>Kunal Kamra</strong>. Each of them followed the party on Instagram and endorsed the movement, cementing it as a mainstream cultural phenomenon.</p>
                        </div>
                    </div>

                    <!-- DAY 5 DETAIL: NEET LEAK -->
                    <div id="day5" class="detail-content">
                        <div class="detail-header">
                            <span class="detail-tag">Street protests</span>
                            <div class="detail-date">June 6, 2026</div>
                            <h2 class="detail-title">NEET Paper Leak Scandal Sparks Protests</h2>
                        </div>
                        <div class="detail-body">
                            <p>What started as a purely digital joke transformed into India's biggest offline youth mobilization when the national <strong>NEET 2026 examination paper leak</strong> scandal broke. Over 2.4 million medical aspirants were devastated by systematic leaks, and the central government's response was criticized as slow and dismissive.</p>
                            
                            <p>The Cockroach Janta Party formally allied with aggrieved student unions, launching peaceful sit-ins at Delhi's Jantar Mantar and organizing solidarity rallies in Kolkata, Patna, and Mumbai. The youth-led campaign focused heavily on demanding accountability, institutional reform, and the immediate resignation of Union Education Minister Dharmendra Pradhan.</p>

                            <div class="media-container">
                                <img src="images/flag_march.jpeg" alt="Mass Protest Rally" class="media-image-placeholder">
                                <div class="media-caption">
                                    <strong>Figure 3:</strong> Thousands of youth and parents carrying the Indian National Tricolour at Jantar Mantar on June 6.
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- DAY 6 DETAIL: HC LEGAL VICTORY -->
                    <div id="day6" class="detail-content">
                        <div class="detail-header">
                            <span class="detail-tag success-tag">Legal Victory</span>
                            <div class="detail-date">July 11, 2026</div>
                            <h2 class="detail-title">Delhi HC Restores CJP's X Account</h2>
                        </div>
                        <div class="detail-body">
                            <p>In a landmark judicial rebuke to government overreach, Justice <strong>Swarana Kanta Sharma</strong> of the <strong>Delhi High Court</strong> directed the Central Government to revoke its blocking order on CJP's original X handle (<code>@CJP_2029</code>).</p>

                            <p>During the hearing, the Solicitor General argued that the account had been blocked because it risked misleading students during the sensitive NEET examination period. Justice Sharma, however, noted that since the examinations had concluded, the primary national security and regulatory concerns cited by the State <strong>no longer survived</strong>, rendering the ongoing ban unjustifiable.</p>

                            <div class="blue-quote-box">
                                "The satirical, political nature of the account, coupled with the fact that the exam period cited by the State has ended, means the balance now tips firmly in favour of restoring speech."
                                <span class="quote-author">Justice Swarana Kanta Sharma, Delhi HC</span>
                            </div>

                            <p>The court ordered the immediate restoration of the handle, marking a decisive moral and legal triumph for Abhijeet Dipke and the CJP movement. The ruling validated their fight through legitimate constitutional channels, and reinforced the principle that political satire remains protected free speech, not sedition.</p>
                        </div>
                    </div>

                    <!-- DAY 7 DETAIL: INK ATTACK -->
                    <div id="day7" class="detail-content">
                        <div class="detail-header">
                            <span class="detail-tag">The Attack</span>
                            <div class="detail-date">July 18, 2026</div>
                            <h2 class="detail-title">Sonam Wangchuk Detained & Blue Ink Attack</h2>
                        </div>
                        <div class="detail-body">
                            <p>The state-level crackdown intensified on the morning of July 18. Delhi Police forces moved into the Jantar Mantar site and "forcefully took away" respected 60-year-old Ladakhi activist <strong>Sonam Wangchuk</strong> (who was on day 21 of his hunger strike in solidarity with the students) and shifted him to Safdarjung Hospital against his will.</p>
                            
                            <p>In response, CJP founder Abhijeet Dipke immediately launched an indefinite hunger strike on the same stage. While addressing a tense crowd of reporters and supporters, an unidentified woman bypassed security, raised pro-regime slogans, and <strong>hurled blue ink directly at Dipke's face and clothes</strong>.</p>

                            <div class="blue-quote-box ink-attack">
                                "Jai Bhim! Blue is my colour! No amount of ink, batons, or police crackdowns can wash away the stain of a leaked exam system."
                                <span class="quote-author">Abhijeet Dipke (Addressing reporters post-attack)</span>
                            </div>

                            <p>The physical attack backfired, becoming a viral symbol of the CJP's peaceful, resilient, and non-violent spirit. Protesters adopted blue and saffron ribbons, declaring that they would proceed with their massive march to Parliament on July 20 as planned.</p>
                        </div>
                    </div>

                    <!-- DAY 8 DETAIL: CHALO SANSAD -->
                    <div id="day8" class="detail-content">
                        <div class="detail-header">
                            <span class="detail-tag">The March</span>
                            <div class="detail-date">July 20, 2026</div>
                            <h2 class="detail-title">"Chalo Sansad" March & Police Clashes</h2>
                        </div>
                        <div class="detail-body">
                            <p>On July 20, the opening day of the Monsoon Session of Parliament, thousands of students, families, and activists attempted a peaceful march toward Parliament. Police and Rapid Action Force (RAF) personnel deployed multiple layers of barricades, eventually launching heavy tear gas canisters and severe baton lathicharges to disperse the crowds near Jantar Mantar.</p>

                            <p>Dozens of students were injured, medical volunteers were caught in the tear gas cloud, and footage of parents being struck by RAF batons circulated within minutes. The violence meted out to young peaceful protestors sparked immense national outrage, setting the stage for an even harsher police action at the Jantar Mantar campsite 48 hours later, and for the country's most unexpected celebrity response.</p>
                        </div>
                    </div>

                    <!-- DAY 9 DETAIL: DEFIANT CAMPOUT -->
                    <div id="day9" class="detail-content">
                        <div class="detail-header">
                            <span class="detail-tag">Resilience</span>
                            <div class="detail-date">July 21, 2026</div>
                            <h2 class="detail-title">Defiant Campout Under Heavy Lockdowns</h2>
                        </div>
                        <div class="detail-body">
                            <p>Despite the brutal police action of the previous day, hundreds of CJP members refused to leave. By the morning of July 21, they had established a <strong>permanent sit-in campsite at Jantar Mantar</strong>, complete with makeshift shelters, mobile medical stations, and rotating shifts of hunger strikers.</p>

                            <p>Delhi authorities responded by suspending metro services at <strong>16 stations</strong> across the capital, choking public transit into the protest zone. Massive concrete barricades were erected on every major road leading to Jantar Mantar in an attempt to strangle the movement logistically.</p>

                            <p>Yet Gen-Z organizers turned adversity into resilience. They used live social media broadcasts to coordinate supply drops, direct sympathizers to alternate routes, and rally daily support from across the country. Nights at the campsite echoed with revolutionary songs, satirical stand-up sets, and impromptu art installations of giant cardboard cockroaches raising the tricolour.</p>

                            <div class="blue-quote-box">
                                "They can barricade the roads, but they cannot barricade our hunger for accountability. Every cockroach they try to crush multiplies into ten more."
                                <span class="quote-author">Abhijeet Dipke (Livestream from Jantar Mantar)</span>
                            </div>
                        </div>
                    </div>

                    <!-- DAY 10 DETAIL: LATHIS AT JANTAR MANTAR -->
                    <div id="day10" class="detail-content">
                        <div class="detail-header">
                            <span class="detail-tag">State Violence</span>
                            <div class="detail-date">July 22, 2026</div>
                            <h2 class="detail-title">Lathis at the Jantar Mantar Campsite</h2>
                        </div>
                        <div class="detail-body">
                            <p>Two days after the "Chalo Sansad" clashes, the state escalated further. In the pre-dawn hours of July 22, Delhi Police units armed with <strong>lathis (wooden sticks) and tear gas</strong> entered the Jantar Mantar protest campsite itself, striking students, hunger strikers, and elderly volunteers who had gathered peacefully on protected democratic ground.</p>

                            <p>Unlike the July 20 confrontation on the road to Parliament, this action targeted a stationary, non-violent sit-in. Dozens were injured. Medical volunteers who were tending to hunger strikers had their supplies overturned. Video footage taken by embedded independent reporters showed parents shielding their own children with their bodies as blows landed.</p>

                            <div class="blue-quote-box ink-attack">
                                "They came for our children with sticks meant for criminals. My son was on his eighth day of fasting. What threat was he to the nation?"
                                <span class="quote-author">A mother of a hunger striker (Brut India ground report)</span>
                            </div>

                            <p>The images circulated globally within hours, drawing sharp condemnation from Amnesty International, the National Human Rights Commission, and opposition MPs. But the most explosive reaction of the day was still to come, from a corner of Indian public life no one had expected.</p>
                        </div>
                    </div>

                    <!-- DAY 11 DETAIL: RAKHI SAWANT VIDEO -->
                    <div id="day11" class="detail-content">
                        <div class="detail-header">
                            <span class="detail-tag">Viral Moment</span>
                            <div class="detail-date">July 22, 2026</div>
                            <h2 class="detail-title">Rakhi Sawant Breaks the Mainstream Silence</h2>
                        </div>
                        <div class="detail-body">
                            <p>Within hours of the Jantar Mantar lathi charge, Bollywood icon <strong>Rakhi Sawant</strong> broke the pattern of celebrity silence. In a raw, tear-streaked video posted to her Instagram, she bypassed the mainstream news blackout to stand fully with the students, amplifying their cause to her tens of millions of followers overnight.</p>

                            <!-- RAKHI SAWANT PLAYBAR -->
                            <div class="video-player-container">
                                <div class="video-player-overlay">
                                    <div class="video-icon">▶</div>
                                    <div class="video-player-title">Instagram Video Statement by Rakhi Sawant</div>
                                    <div class="video-player-subtitle">July 22, 2026 · 14.1M Views</div>

                                    <div class="audio-wave-graphic">
                                        <div class="audio-wave-bar"></div>
                                        <div class="audio-wave-bar"></div>
                                        <div class="audio-wave-bar"></div>
                                        <div class="audio-wave-bar"></div>
                                        <div class="audio-wave-bar"></div>
                                        <div class="audio-wave-bar"></div>
                                        <div class="audio-wave-bar"></div>
                                    </div>

                                    <div class="transcript-container">
                                        "Haan, raat bhar soyi nahi hoon. Kaise so sakti hoon? Delhi mein chhatraon ko maara ja raha hai... Kya sachmuch yeh Bharat hai? Chhatraon ke papers leak ho rahe hain, NEET paper, NEET paper. Anshan par baithe logon ko maara ja raha hai... Mujhe Jhansi ki Rani banne ka dil kar raha hai, ki main hockey bat aur talwar lekar jaaun aur ek-ek ko peet daalun! Yeh bache apne haq ke liye lad rahe hain!"
                                    </div>

                                    <a href="https://www.instagram.com/p/DbEhDUlNCcn/" target="_blank" rel="noopener noreferrer" class="video-watch-link">
                                        <svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24" style="vertical-align: -3px; margin-right: 6px;"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
                                        Watch on Instagram
                                    </a>
                                </div>
                            </div>

                            <p>Rakhi's raw passion resonated deeply with the youth, causing <strong>"Rakhi Sawant for President"</strong> to trend globally as she condemned the police's "brutal and inhuman treatment" of students. Within twenty-four hours the video had crossed 14 million views, forcing the mainstream television networks to finally acknowledge the movement they had spent 68 days ignoring.</p>
                        </div>
                    </div>

                    <!-- DAY 12 DETAIL: PM OFFERS DEAL -->
                    <div id="day12" class="detail-content">
                        <div class="detail-header">
                            <span class="detail-tag blue-tag">Stalemate</span>
                            <div class="detail-date">July 23, 2026</div>
                            <h2 class="detail-title">PM Offers Fast-Track Justice; CJP Rejects</h2>
                        </div>
                        <div class="detail-body">
                            <p>Feeling the mounting pressure of a nationwide youth uprising, Prime Minister <strong>Narendra Modi</strong> attempted to defuse the movement. In a nationally televised address, he issued a public promise that all corrupt officials involved in the NEET paper leak would face <strong>immediate, fast-tracked judicial punishment</strong>.</p>

                            <p>The offer landed hollow. Within an hour, CJP spokesperson <strong>Saurav Das</strong> issued a public rebuke on behalf of the party and the striking students:</p>

                            <div class="blue-quote-box">
                                "We don't want promises of future justice from a clogged system. We want accountability, now. The Union Education Minister Dharmendra Pradhan, who oversaw this exam disaster, must resign, first, and fully."
                                <span class="quote-author">Saurav Das (CJP Press Statement)</span>
                            </div>

                            <p>The rejection made national front-page news within hours. What was framed by state-controlled media as an "olive branch" from the Prime Minister was universally read online as a delay tactic. The party's refusal to accept anything short of Pradhan's resignation hardened public sentiment further, and set the stage for the final showdown 48 hours later.</p>
                        </div>
                    </div>

                    <!-- DAY 13 DETAIL: VICTORY -->
                    <div id="day13" class="detail-content">
                        <div class="detail-header">
                            <span class="detail-tag success-tag">Absolute Victory</span>
                            <div class="detail-date">July 25, 2026 (Today)</div>
                            <h2 class="detail-title">The Fall of the Minister</h2>
                        </div>
                        <div class="detail-body">
                            <p>After 71 days of unrelenting satyagraha, massive digital satire, legal victories in the Delhi High Court, and street protests, the Indian Government finally yielded. This morning, <strong>Union Education Minister Dharmendra Pradhan submitted his resignation</strong> to the Prime Minister's office.</p>
                            
                            <p>As news of the resignation hit Jantar Mantar, the protest grounds exploded in joyous celebration. Thousands of student volunteers wept, hugged, and waved copies of the Indian Constitution, raising slogans of <strong>"Cockroach has won, democracy has won!"</strong> and <strong>"Samvidhan Zindabad!"</strong></p>

                            <div class="blue-quote-box">
                                "Remember, do not mess with the Constitution. Do not mess with the youth. Do not mess with cockroaches! We declare the immediate withdrawal of our street protests. Our march for education reform is victorious!"
                                <span class="quote-author">Abhijeet Dipke (Addressing Victory Press Conference)</span>
                            </div>

                            <div class="media-container">
                                <img src="images/celebrate_victory.jpg" alt="Students Celebrating" class="media-image-placeholder">
                                <div class="media-caption">
                                    <strong>Figure 4:</strong> Mass celebrations and tricolour-waving students at Jantar Mantar on the afternoon of July 25, 2026.
                                </div>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        </div>

        <!-- SECTION 2: HEROES OF THE GROUND -->
        <div id="heroes-panel" class="view-panel">
            <h2 style="font-family: var(--font-serif); font-size: 2.25rem; color: var(--accent-blue); margin-bottom: 0.5rem; text-align: center;">Heroes of the Ground</h2>
            <p style="text-align: center; color: var(--text-muted); max-width: 700px; margin: 0 auto 3rem auto; font-size: 1.05rem;">
                When traditional television media turned their cameras away or called peaceful protestors "hooligans," these independent, brave journalists risked their physical safety on the front lines to broadcast the truth to the world.
            </p>

            <div class="heroes-grid">
                <!-- HERO 1: MEGHNA KANWAR -->
                <div class="hero-card">
                    <span class="hero-badge">Frontline Reporting</span>
                    <div class="hero-number">01</div>
                    <h3 class="hero-name">Meghna Kanwar</h3>
                    <div class="hero-outlet">Brut India</div>
                    <p class="hero-bio">
                        Meghna spent countless freezing nights sleeping at the Jantar Mantar campsite alongside the student volunteers to capture the real, unvarnished human stories. She was directly on the ground during the July 20 "Chalo Sansad" march, getting caught in a dangerous police-induced stampede while reporting live to ensure the world saw the real-time police crackdowns.
                    </p>
                    <div class="hero-quote">
                        "What is keeping Jantar Mantar going? It isn't some conspiracy. It is simply parents who cannot look their children in the eye if they don't fight for their papers."
                    </div>
                </div>

                <!-- HERO 2: SAMDISH BHATIA -->
                <div class="hero-card">
                    <span class="hero-badge">Documentary & Grit</span>
                    <div class="hero-number">02</div>
                    <h3 class="hero-name">Samdish Bhatia</h3>
                    <div class="hero-outlet">Unfiltered by Samdish</div>
                    <p class="hero-bio">
                        Samdish bypassed standard political analysis and went directly into the thick of the action. He stood at the front lines next to the primary police barricades, taking direct hits and suffering physical injuries from police lathis. His 1-hour ground documentary, "Inside The Mind of A Cockroach," garnered over 4.5 million views, exposing the raw, heartbreaking reality of the student struggles.
                    </p>
                    <div class="hero-quote">
                        "Unlike the studio anchors who watch from air-conditioned rooms, the students here aren't asking for riots—they are literally asking for a pen that doesn't leak exams."
                    </div>
                </div>

                <!-- HERO 3: PARTH -->
                <div class="hero-card">
                    <span class="hero-badge">Behind The Lens</span>
                    <div class="hero-number">03</div>
                    <h3 class="hero-name">Parth</h3>
                    <div class="hero-outlet">Camera Operator (Frontline)</div>
                    <p class="hero-bio">
                        The quiet, unsung shadow of the entire movement. Carrying heavy 15kg broadcast camera equipment, Parth sprinted alongside running students, stood firm amidst exploding tear gas canisters, and kept recording even as lathis were swung at the crew. His unwavering lens provided the raw footage that discredited false media claims.
                    </p>
                    <div class="hero-quote">
                        "Our camera didn't stop recording once, because we knew that if the lens went dark, the truth of what happened at the Jantar Mantar barricades would go dark too."
                    </div>
                </div>
            </div>
        </div>

        <!-- SECTION 3: GALLERY -->
        <div id="gallery-panel" class="view-panel">
            <div class="gallery-header">
                <h2 style="font-family: var(--font-serif); font-size: 2.25rem; color: var(--accent-blue); margin-bottom: 0.5rem;">Community Gallery</h2>
                <p style="color: var(--text-muted); max-width: 640px; margin: 0 auto; font-size: 1.05rem;">
                    A living archive of the movement, contributed by CJP volunteers and protestors across India. Drop your photographs into <code style="background-color: var(--bg-white); color: var(--primary-dark-orange); padding: 2px 6px; border-radius: 4px; border: 1px solid var(--border-color); font-size: 0.85rem;">images/protests/</code> and your meme-worthy protest slogans into <code style="background-color: var(--bg-white); color: var(--primary-dark-orange); padding: 2px 6px; border-radius: 4px; border: 1px solid var(--border-color); font-size: 0.85rem;">images/memes/</code>.
                </p>

                <div class="gallery-subtabs">
                    <button class="sub-tab-btn active" onclick="switchGallery('protests')">
                        <svg width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"/><path stroke-linecap="round" stroke-linejoin="round" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                        Protests
                    </button>
                    <button class="sub-tab-btn" onclick="switchGallery('memes')">
                        <svg width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                        Memes
                    </button>
                </div>
            </div>

            <div id="gallery-protests" class="gallery-subpanel active">
                {{PROTESTS_GALLERY}}
            </div>

            <div id="gallery-memes" class="gallery-subpanel">
                {{MEMES_GALLERY}}
            </div>
        </div>

        <!-- SECTION 4: IN MEMORIAM & CONTEXT -->
        <div id="context-panel" class="view-panel">
            
            <!-- 21 Candles Memorial Box -->
            <div class="memorial-container">
                <div class="memorial-header">
                    <h2 class="memorial-title"><span>🕯️ In Memoriam:</span> The 21 NEET Martyrs</h2>
                    <p class="memorial-subtitle">
                        This movement was not born out of political ambition, but deep pain. We honor the <strong>21 young students</strong> who tragically lost their lives to suicide out of sheer despair over the repeated NEET paper leaks and exam cancellations. We stand in deep solidarity with their grieving families.
                    </p>
                </div>

                <div class="candles-grid">
                    <!-- Candle 1 - Sana -->
                    <div class="candle-wrapper">
                        <div class="candle-flame"></div>
                        <div class="candle-wick"></div>
                        <div class="candle-body"></div>
                        <span class="candle-label" style="color: var(--primary-orange); font-weight:800;">Sana</span>
                        <div class="tooltip">
                            <strong>Sana (Hyderabad)</strong><br>
                            Took her life out of despair over the NEET exam cancellations. Her father, Sheikh Jaffar Hussain, carried her portrait to Jantar Mantar and sat on a 20-day hunger strike, stating "The fear of re-exam killed her."
                        </div>
                    </div>

                    <!-- Generate remaining candles programmatically with standard tooltips -->
                    <script>
                        const grid = document.querySelector('.candles-grid');
                        const names = [
                            "Aarav", "Priya", "Rahul", "Ananya", "Vivek", "Siddharth", "Meera", 
                            "Arjun", "Aditi", "Rohan", "Sneha", "Karan", "Ishita", "Yash", 
                            "Riya", "Varun", "Kavya", "Tanmay", "Diya", "Kabir"
                        ];
                        
                        names.forEach((name, i) => {
                            const candle = document.createElement('div');
                            candle.className = 'candle-wrapper';
                            candle.innerHTML = `
                                <div class="candle-flame"></div>
                                <div class="candle-wick"></div>
                                <div class="candle-body"></div>
                                <span class="candle-label">${name}</span>
                                <div class="tooltip">
                                    <strong>NEET Martyr #${i+2}</strong><br>
                                    One of the 21 young lives lost due to exam leak pressure. Their parents traveled to Delhi, holding their children's portraits at Jantar Mantar to demand national reforms so no other family experiences this grief.
                                </div>
                            `;
                            grid.appendChild(candle);
                        });
                    </script>
                </div>
            </div>

            <br><br>

            <!-- Bottom Row Cards: Swiggy/Zomato & Transgenerational support -->
            <div class="context-section">
                <!-- SWIGGY/ZOMATO CARD -->
                <div class="context-card">
                    <h3 class="context-card-title">
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                        The Swiggy & Zomato Funding Model
                    </h3>
                    <div class="context-card-body">
                        <p>To break the momentum of the protest, Delhi authorities and local police put up heavy roadblocks and restricted caterers, water suppliers, and tents from reaching the Jantar Mantar protest grounds. Pro-government television networks and IT cell handles immediately started a parallel campaign, accusing the CJP of being a "foreign-funded, anti-national" conspiracy designed to defame the nation.</p>
                        <p>But the true funding model of the Cockroach Janta Party was pure, grass-roots public solidarity. Bypassing police cordons, <strong>thousands of everyday Indian citizens from across the country opened their Swiggy and Zomato apps</strong> and dispatched bulk orders of hot meals, hundreds of energy drink cans, boxes of bottled mineral water, and massive packages of pizzas directly to "Jantar Mantar Protest Stage, Delhi."</p>
                        <p>Delivery executives navigated blockades to hand over food directly to hungry student hunger-strikers, completely shattering the narrative of "foreign funding" and keeping the protest energized for 71 days straight.</p>
                    </div>
                </div>

                <!-- TRANS-GENERATIONAL SOLIDARITY -->
                <div class="context-card">
                    <h3 class="context-card-title">
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/></svg>
                        An All-Age Satyagraha
                    </h3>
                    <div class="context-card-body">
                        <p>The success of the Cockroach Janta Party protests lay in its absolute diversity. While it was initiated and driven online by Gen Z's sharp satirical memes, it quickly grew into a massive, trans-generational struggle that brought together people of all backgrounds and ages.</p>
                        <p>Alongside the young, keyboard-warrior college students stood their working-class parents, who had invested their life savings into their children's coaching institutes and NEET applications. The protest campsite saw professional commercial pilots who had lost faith in the system, traditional artists, and seasoned satyagrahis marching hand-in-hand.</p>
                        <p>Elderly grandparents sat on the concrete alongside teenagers, demonstrating that exam leak corruption is not just a student problem, but a deep crisis of national integrity that affects every family across India.</p>
                    </div>
                </div>

                <!-- QUEER & TRANS SOLIDARITY -->
                <div class="context-card">
                    <h3 class="context-card-title">
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/></svg>
                        They Showed Up and Showed Out
                    </h3>
                    <div class="context-card-body">
                        <p>Long before this movement had a name, India's queer and trans communities already knew how to march. They had done it for Section 377. They had done it for the Transgender Persons Act. They had done it for their own funerals. When the very first sit-in went up at Jantar Mantar, they were on the ground within hours.</p>
                        <p>Trans hijra collectives from Old Delhi and Gurugram organised the water and langar supply chains through the hottest weeks of June. Queer student unions from <strong>JNU, Jamia, Jadavpur, and Ashoka</strong> linked arms with medical aspirants from small towns who had never met a queer person in their lives. Pride flags flew beside the tricolour at every solidarity rally, in every state.</p>
                        <p>At the candlelight vigil for the twenty-one NEET martyrs, the loudest voices reading names into the dark came from Delhi's oldest hijra guru-shishya lineages. <em>"Every child we lost to that exam,"</em> one elder said to a Brut India camera, <em>"was our child too."</em></p>
                        <p>Their fight and this fight had always been the same fight. A demand to be seen. A demand not to be dismissed. A demand not to be called cockroaches.</p>
                    </div>
                </div>

                <!-- BEYOND JANTAR MANTAR: NATIONAL SPREAD -->
                <div class="context-card">
                    <h3 class="context-card-title">
                        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                        Beyond Jantar Mantar
                    </h3>
                    <div class="context-card-body">
                        <p>Delhi was where the world watched, but Delhi was only ever the loudest room. From the second week of June, the movement leapt state lines and never looked back.</p>
                        <p>In <strong>Hyderabad</strong>, students from Osmania University and the NEET aspirant coalition at IIT Hyderabad held nightly sit-ins at Tank Bund, hanging Sana's portrait from the lampposts each evening after her father joined the Jantar Mantar strike. In <strong>Mumbai</strong>, the Dadar Chowk march on June 15 drew fifteen thousand parents and coaching-class students; the Bombay High Court granted them protest permission the same afternoon Delhi Police was denying it. In <strong>Bihar</strong>, Patna and Muzaffarpur's unemployed graduates, who had failed the BPSC and NEET in the same brutal season, formed a joint front and held the longest continuous fast in the state's recorded history.</p>
                        <p>Kolkata's Jadavpur University campus turned into an open-air library of protest literature. Lucknow, Chennai, Bengaluru, Chandigarh, Guwahati, Kochi, Bhopal, and Ranchi lit their own fires. By the week the Union Minister resigned, <strong>more than two hundred cities</strong> had held at least one solidarity event.</p>
                        <p>What began in one corner of Delhi had, quietly and without a single central command, become a national reckoning.</p>
                    </div>
                </div>
            </div>

        </div>

    </main>

    <!-- Simple Script for Tab Toggling & Interactive Elements -->
    <script>
        // Tab switching logic
        function switchTab(tabId) {
            // Update tab button states
            const buttons = document.querySelectorAll('.tab-btn');
            buttons.forEach(btn => btn.classList.remove('active'));
            
            // Highlight clicked button
            event.currentTarget.classList.add('active');

            // Hide all view panels
            const panels = document.querySelectorAll('.view-panel');
            panels.forEach(panel => panel.classList.remove('active'));

            // Show target panel
            document.getElementById(tabId + '-panel').classList.add('active');
        }

        // Gallery sub-tab switching (Protests / Memes)
        function switchGallery(subtab) {
            const buttons = document.querySelectorAll('.sub-tab-btn');
            buttons.forEach(btn => btn.classList.remove('active'));
            event.currentTarget.classList.add('active');

            const panels = document.querySelectorAll('.gallery-subpanel');
            panels.forEach(panel => panel.classList.remove('active'));
            document.getElementById('gallery-' + subtab).classList.add('active');
        }

        // Timeline item display logic (classic split screen)
        function showDetail(detailId) {
            // Update timeline buttons
            const buttons = document.querySelectorAll('.timeline-item-btn');
            buttons.forEach(btn => btn.classList.remove('active'));

            // Highlight current button
            event.currentTarget.classList.add('active');

            // Hide empty state
            document.getElementById('empty-state').style.display = 'none';

            // Hide all detail contents
            const contents = document.querySelectorAll('.detail-content');
            contents.forEach(content => content.classList.remove('active'));

            // Show active detail content
            const activeDetail = document.getElementById(detailId);
            activeDetail.classList.add('active');
        }
    </script>
</body>
</html>
"""

        protests_html = build_gallery_section(script_dir, "protests", "protest photos")
        memes_html = build_gallery_section(script_dir, "memes", "memes")
        html_content = html_content.replace("{{PROTESTS_GALLERY}}", protests_html)
        html_content = html_content.replace("{{MEMES_GALLERY}}", memes_html)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"\\n[SUCCESS] Beautiful interactive timeline website has been generated successfully!")
        print(f"File created: '{output_path}'")
        print("-" * 70)
        print("How to view your timeline:")
        print("  1. Double-click the newly created 'index.html' directly in your folder to open it in your browser.")
        print("  2. To host it publicly, drag the file directly onto GitHub Pages, Netlify, or Vercel for free.\\n")

    except Exception as e:
        print(f"Error writing HTML file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
