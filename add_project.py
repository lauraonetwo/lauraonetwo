import argparse
import re

def convert_to_embed_link(youtube_link):
    match = re.match(r".*v=([^&]+)", youtube_link)
    if match:
        video_id = match.group(1)
        return f"https://www.youtube.com/embed/{video_id}"
    else:
        raise ValueError("Youtube link is not valid. Please provide a valid link")

def add_project(categories, video_link, title, more_info_link, image_path):
    portfolio_file = "docs/portfolio.html"
    embed_link = convert_to_embed_link(video_link)

    more_info_html = f'data-redirect="{more_info_link}"' if more_info_link else 'data-redirect=""'

    new_project_html = f"""
    <div class="col mb-4 portfolio-item {categories}">
        <a href="#" class="image-link" data-bs-toggle="modal" data-bs-target="#videoModal"
            data-video="{embed_link}"
            {more_info_html}
            title="{title}">
            <img src="{image_path}" class="img-fluid" alt="{title}"></a>
    </div>
    """

    with open(portfolio_file, "r", encoding="utf-8") as file:
        content = file.read()

    grid_start_tag = '<div class="grid p-0 clearfix row row-cols-2 row-cols-lg-3 row-cols-xl-4" data-aos="fade-up">'
    if grid_start_tag in content:
        updated_content = content.replace(
            grid_start_tag,
            f'{grid_start_tag}\n{new_project_html}'
        )
    else:
        raise ValueError("Could not find the grid start tag in the portfolio file")

    with open(portfolio_file, "w", encoding="utf-8") as file:
        file.write(updated_content)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add a new project to the portfolio.")
    parser.add_argument("--categories", required=True, help="Categories for the project (e.g., 'all prog gamea')")
    parser.add_argument("--video_link", required=True, help="YouTube video link")
    parser.add_argument("--title", required=True, help="Title of the project")
    parser.add_argument("--more_info_link", required=False, help="Link for more information (optional)")
    parser.add_argument("--image_path", required=True, help="Path to the project image")

    args = parser.parse_args()
    add_project(args.categories, args.video_link, args.title, args.more_info_link, args.image_path)
