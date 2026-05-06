import os
import re

nav_html = """    <!-- Navigation -->
    <nav class="fixed w-full z-50 transition-all duration-500 py-6" id="mainNav">
        <div class="max-w-7xl mx-auto px-6 lg:px-8">
            <div class="flex justify-between items-center h-16 glass rounded-2xl px-8 shadow-sm border border-slate-200/50" style="background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);">
                <a href="index.html" class="flex items-center gap-4 cursor-pointer" style="text-decoration: none;">
                    <img src="https://static.wixstatic.com/media/5349ce_c4d8e09464dc407191330009a29ba4cf~mv2.png" alt="Logo" class="h-10 w-auto" style="height: 40px;">
                    <span class="font-extrabold text-2xl tracking-tighter hidden sm:block" style="color: #0f172a; font-weight: 800;">AIC-JKLU</span>
                </a>
                <div class="hidden md:flex space-x-10 items-center font-bold text-slate-600">
                    <a href="index.html" class="hover:text-[#751FFF] transition-colors" style="text-decoration: none;">Home</a>
                    <a href="index.html#programs" class="hover:text-[#751FFF] transition-colors" style="text-decoration: none;">Programs</a>
                    <div class="dropdown-parent relative" style="position: relative;">
                        <a href="#" class="text-[#751FFF] transition-colors flex items-center gap-1" style="text-decoration: none;">
                            Stakeholders
                            <i data-lucide="chevron-down" class="w-4 h-4"></i>
                        </a>
                        <div class="dropdown-menu absolute top-full left-1/2 -translate-x-1/2 mt-3 w-56 glass rounded-2xl shadow-2xl border border-slate-200/50 overflow-hidden" style="background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(16px);">
                            <a href="mentors.html" class="flex items-center gap-3 px-6 py-4 hover:bg-purple-50 transition-colors text-slate-700 hover:text-[#751FFF] font-semibold" style="text-decoration: none; color: #334155;">
                                <i data-lucide="lightbulb" class="w-5 h-5 text-orange-500"></i>
                                Mentors
                            </a>
                            <a href="team.html" class="flex items-center gap-3 px-6 py-4 hover:bg-purple-50 transition-colors text-slate-700 hover:text-[#751FFF] font-semibold border-t border-slate-100" style="text-decoration: none; color: #334155;">
                                <i data-lucide="users" class="w-5 h-5 text-purple-500"></i>
                                Team
                            </a>
                            <a href="partners.html" class="flex items-center gap-3 px-6 py-4 hover:bg-purple-50 transition-colors text-slate-700 hover:text-[#751FFF] font-semibold border-t border-slate-100" style="text-decoration: none; color: #334155;">
                                <i data-lucide="handshake" class="w-5 h-5 text-blue-500"></i>
                                Partners
                            </a>
                        </div>
                    </div>
                    <a href="index.html#aarohan" class="hover:text-[#751FFF] transition-colors" style="text-decoration: none;">Aarohan 3.0</a>
                    <a href="index.html#register" class="bg-gradient-to-r from-[#F27124] to-[#ff8c42] text-white px-8 py-2.5 rounded-xl hover:shadow-lg hover:shadow-orange-500/30 transition-all hover:-translate-y-1" style="text-decoration: none; background: linear-gradient(135deg, #F27124 0%, #ff8c42 100%); color: white;">Apply Now</a>
                </div>
            </div>
        </div>
    </nav>"""

dropdown_css = """
        /* Nav dropdown */
        .dropdown-menu {
            opacity: 0;
            visibility: hidden;
            transform: translateY(10px);
            transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
            position: absolute;
            z-index: 50;
        }

        .dropdown-parent:hover .dropdown-menu {
            opacity: 1;
            visibility: visible;
            transform: translateY(0);
        }
"""

directory = r"c:\Users\KAILASH\Downloads\website"

html_files = [
    "index.html", 
    "index1.html", 
    "leap.html", 
    "mentors.html", 
    "team.html", 
    "partners.html", 
    "rise.html",
    "incubation.html",
    "accelerator.html",
    "mywork.html",
    "final.html"
]

for filename in html_files:
    filepath = os.path.join(directory, filename)
    if not os.path.exists(filepath):
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # check if <nav exists
    # but some have <nav> some have <nav class="...">
    # re.sub strategy: find block starting with <nav and ending with </nav>
    
    # if there is a nav, replace the FIRST nav
    if re.search(r'<nav[^>]*>.*?</nav>', content, flags=re.DOTALL | re.IGNORECASE):
        # We might have <!-- Navigation --> right before it
        content = re.sub(r'<!--\s*Navigation\s*-->\s*<nav[^>]*>.*?</nav>', nav_html, content, flags=re.DOTALL | re.IGNORECASE)
        # In case the exact comment didn't match
        if nav_html not in content:
            content = re.sub(r'<nav[^>]*>.*?</nav>', nav_html, content, flags=re.DOTALL | re.IGNORECASE, count=1)
    else:
        # no nav, inject after <body ...>
        content = re.sub(r'(<body[^>]*>)', r'\1\n' + nav_html, content, flags=re.IGNORECASE)

    # ensure Dropdown CSS
    if '.dropdown-menu {' not in content:
        if '</style>' in content:
            content = content.replace('</style>', dropdown_css + '\n    </style>')
        else:
            content = content.replace('</head>', '<style>\n' + dropdown_css + '\n</style>\n</head>')

    # ensure Tailwind
    if 'tailwindcss' not in content:
        content = content.replace('</head>', '    <script src="https://cdn.tailwindcss.com"></script>\n</head>')

    # ensure Lucide
    if 'lucide' not in content:
        content = content.replace('</head>', '    <script src="https://unpkg.com/lucide@latest"></script>\n</head>')

    # ensure lucide.createIcons();
    if 'lucide.createIcons()' not in content:
        # Check if there is a closing body tag
        if '</body>' in content:
            content = content.replace('</body>', '    <script>\n        lucide.createIcons();\n    </script>\n</body>')
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Updated {filename}")
