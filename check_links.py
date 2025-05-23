import json
import os

# Input from the previous step
links_data_str = """
[{"file": "src/components/Footer.astro", "url": "/rss.xml", "type": "internal"}, 
 {"file": "src/components/Nav.astro", "url": "/", "type": "internal"}, 
 {"file": "src/content/blog/custom-mdx-examples.mdx", "url": "https://github.com/vikas5914/Astrofolio/blob/main/src/components/mdx", "type": "external"}, 
 {"file": "src/content/blog/custom-mdx-examples.mdx", "url": "https://astro.build/", "type": "external"}, 
 {"file": "src/content/blog/custom-mdx-examples.mdx", "url": "https://bun.sh/", "type": "external"}, 
 {"file": "src/content/blog/custom-mdx-examples.mdx", "url": "https://docs.astro.build/en/guides/images/", "type": "external"}, 
 {"file": "src/content/blog/custom-mdx-examples.mdx", "url": "https://github.com/vikas5914/Astrofolio/blob/main/src/components/mdx/ImageGrid.astro", "type": "external"}, 
 {"file": "src/content/blog/custom-mdx-examples.mdx", "url": "https://github.com/tsriram/astro-tweet/", "type": "external"}, 
 {"file": "src/content/blog/custom-mdx-examples.mdx", "url": "https://astro-embed.netlify.app/", "type": "external"}, 
 {"file": "src/content/blog/custom-mdx-examples.mdx", "url": "https://react-wrap-balancer.vercel.app/", "type": "external"}, 
 {"file": "src/content/blog/custom-mdx-examples.mdx", "url": "https://github.com/vikas5914/Astrofolio/blob/main/src/components/mdx/Table.astro", "type": "external"}, 
 {"file": "src/content/blog/custom-mdx-examples.mdx", "url": "https://katex.org/", "type": "external"}, 
 {"file": "src/content/blog/custom-mdx-examples.mdx", "url": "https://github.com/vikas5914/Astrofolio/blob/main/src/components/mdx/Callout.astro", "type": "external"}, 
 {"file": "src/content/blog/custom-mdx-examples.mdx", "url": "https://astrofolio-astro.vercel.app/", "type": "external"}, 
 {"file": "src/content/blog/custom-mdx-examples.mdx", "url": "https://astrofolio-astro.vercel.app/", "type": "external"}, 
 {"file": "src/content/blog/custom-mdx-examples.mdx", "url": "/opengraph-image.png", "type": "internal_image"}, 
 {"file": "src/content/blog/custom-mdx-examples.mdx", "url": "/opengraph-image.png", "type": "internal_image"}, 
 {"file": "src/content/blog/custom-mdx-examples.mdx", "url": "/photos/photo1.jpg", "type": "internal_image_asset"}, 
 {"file": "src/content/blog/custom-mdx-examples.mdx", "url": "/photos/photo2.jpg", "type": "internal_image_asset"}, 
 {"file": "src/content/blog/custom-mdx-examples.mdx", "url": "/photos/photo3.jpg", "type": "internal_image_asset"}, 
 {"file": "src/content/blog/custom-mdx-examples.mdx", "url": "/photos/photo1.jpg", "type": "internal_image_asset"}, 
 {"file": "src/content/blog/custom-mdx-examples.mdx", "url": "/photos/photo2.jpg", "type": "internal_image_asset"}, 
 {"file": "src/content/blog/custom-mdx-examples.mdx", "url": "/photos/photo3.jpg", "type": "internal_image_asset"}, 
 {"file": "src/content/blog/getting-started.mdx", "url": "https://vercel.com/new/clone?repository-url=https://github.com/vikas5914/Astrofolio", "type": "external"}, 
 {"file": "src/content/blog/getting-started.mdx", "url": "https://github.com/vikas5914/Astrofolio", "type": "external"}, 
 {"file": "src/content/blog/getting-started.mdx", "url": "https://vercel.com/button", "type": "external"}, 
 {"file": "src/content/blog/getting-started.mdx", "url": "https://bun.sh", "type": "external"}, 
 {"file": "src/content/blog/getting-started.mdx", "url": "http://localhost:4321/", "type": "external"}, 
 {"file": "src/content/blog/getting-started.mdx", "url": "https://vercel.com/docs/analytics/quickstart", "type": "external"}, 
 {"file": "src/content/blog/getting-started.mdx", "url": "/rss.xml", "type": "internal"}, 
 {"file": "src/pages/index.astro", "url": "https://econ.au.dk/", "type": "external"}]
"""

links_data = json.loads(links_data_str)

commands_to_run = []
broken_links_report = []

# These are paths that ls() would list at the root of the repo
# We need a more comprehensive list from the initial ls()
# For now, using common locations.
repo_root_files_and_dirs = [
    "public/",
    "src/",
    "README.md" 
    # Add other top-level items if known, e.g. from a previous full ls()
]

def path_exists_in_ls_output(path_to_check, ls_output_lines):
    # Exact match for files, prefix match for directories
    if path_to_check.endswith("/"): # It's a directory
        return any(entry.startswith(path_to_check) for entry in ls_output_lines)
    else: # It's a file
        return path_to_check in ls_output_lines

for link_info in links_data:
    file_path = link_info["file"]
    original_url = link_info["url"]
    link_type = link_info["type"]

    url = original_url.strip()
    command = None

    if link_type == "external":
        command = f'view_text_website(url="{url}")'
    elif link_type.startswith("internal"):
        # Try to determine the correct absolute path for ls()
        abs_link_path = ""
        
        # Astro specific: links starting with / are often relative to `public` or `src/pages`
        if url.startswith("/"):            
            if any(url.endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".gif", ".svg", ".pdf", ".ico", ".webmanifest"]): # typical public assets
                abs_link_path = "public" + url
            elif url == "/": # Special case for root link
                 abs_link_path = "src/pages/index.astro" # Default page
            elif url.endswith(".xml"): # RSS feeds are often generated in public or at root
                 abs_link_path = "public" + url # A common place, or could be at root
            else:
                # Could be a page like /blog, /about, etc.
                # These usually map to src/pages/blog/index.astro or src/pages/about.astro (or src/pages/about/index.astro)
                # This logic is simplified and might need adjustment based on routing patterns.
                potential_path_index = "src/pages" + url + "/index.astro"
                potential_path_direct = "src/pages" + url + ".astro"
                # We need to be able to choose which one, for now, we'll generate commands for both if ambiguous
                # or rely on a more robust check later
                # For simplicity, let's assume /something maps to /something.astro or /something/index.astro
                # This part is tricky without knowing the exact routing or having ls() output for src/pages
                abs_link_path = "src/pages" + url + ".astro" # Default guess
                # A more robust solution would be to check existence of both potential_path_index and potential_path_direct
                # and pick the one that exists. Or, if this is a content collection slug, it's different.
                if url.endswith("/"): # e.g. /blog/
                    abs_link_path = "src/pages" + url.rstrip("/") + "/index.astro"
                else: # e.g. /blog or /blog/post-slug
                    # This could be /blog.astro or /blog/index.astro or /blog/[...slug].astro for a collection
                    # The script needs to be smarter or we need to manually inspect ls output
                    abs_link_path = "src/pages" + url + ".astro" # Defaulting to .astro for non-trailing slash

        else: # Relative path
            # Resolve relative to the current file's directory
            current_file_dir = os.path.dirname(file_path)
            resolved_path = os.path.normpath(os.path.join(current_file_dir, url))
            # ls() operates from repo root, so path should be from root
            abs_link_path = resolved_path
            
        # Normalize path for ls (remove ./)
        abs_link_path = os.path.normpath(abs_link_path)
        if abs_link_path.startswith("./"):
            abs_link_path = abs_link_path[2:]

        command = f'ls("{os.path.dirname(abs_link_path)}")' # List the parent dir to check existence
        # We store the full path we expect to find in the ls output
        link_info["expected_path_in_ls"] = abs_link_path

    if command:
        commands_to_run.append({
            "file": file_path,
            "url": original_url,
            "type": link_type,
            "command": command,
            "expected_path_in_ls": link_info.get("expected_path_in_ls")
        })

# Output the commands as a JSON string to be parsed by the agent
print(json.dumps(commands_to_run))

