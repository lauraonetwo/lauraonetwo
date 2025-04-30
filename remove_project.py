import argparse
from bs4 import BeautifulSoup

def remove_project_by_image(image_name):
    portfolio_file = "docs/portfolio.html"
    image_path = f"images/{image_name}"

    with open(portfolio_file, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    removed = False
    for div in soup.select('div.col.mb-4.portfolio-item'):
        img_tag = div.find('img')
        if img_tag and img_tag.get('src') == image_path:
            div.decompose()
            removed = True
            break

    if not removed:
        raise ValueError(f"Could not find the image '{image_path}' in the portfolio file")

    with open(portfolio_file, "w", encoding="utf-8") as file:
        file.write(str(soup))

    print(f"The project with image '{image_path}' has been removed from the portfolio")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove a project from the portfolio by image name")
    parser.add_argument("--image", required=True, help="Name of the image to remove (e.g., 'project_image.jpg')")

    args = parser.parse_args()
    remove_project_by_image(args.image)
