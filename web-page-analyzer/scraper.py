import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_page(url):

    response = requests.get(
        url,
        timeout=10
    )

    soup = BeautifulSoup(
        response.content,
        "html.parser"
    )

    return response, soup


def analyze_page(url):

    response, soup = get_page(url)

    # -----------------------------
    # Title
    # -----------------------------

    if soup.title:
        title = soup.title.get_text(strip=True)
    else:
        title = "No title found"

    # -----------------------------
    # Headings
    # -----------------------------

    heading_elements = soup.find_all(
        ["h1", "h2", "h3", "h4", "h5", "h6"]
    )

    headings = []

    for heading in heading_elements:

        text = heading.get_text(
            " ",
            strip=True
        )

        if text:
            headings.append({
                "tag": heading.name,
                "text": text
            })

    # -----------------------------
    # Paragraphs
    # -----------------------------

    paragraph_elements = soup.find_all("p")

    paragraphs = []

    for paragraph in paragraph_elements:

        text = paragraph.get_text(
            " ",
            strip=True
        )

        if text:
            paragraphs.append(text)

    # -----------------------------
    # Links
    # -----------------------------

    link_elements = soup.find_all("a")

    links = []

    for link in link_elements:

        text = link.get_text(
            " ",
            strip=True
        )

        href = link.get("href")

        if href:

            full_url = urljoin(
                response.url,
                href
            )

            links.append({
                "text": text if text else "No text",
                "url": full_url
            })

    # -----------------------------
    # Images
    # -----------------------------

    image_elements = soup.find_all("img")

    images = []

    for image in image_elements:

        src = image.get("src")

        if src:

            full_url = urljoin(
                response.url,
                src
            )

            images.append({
                "alt": image.get("alt", "No alt text"),
                "url": full_url
            })



  # -----------------------------
    # Tables
    # -----------------------------

    table_elements = soup.find_all("table")

    tables = []

    for table in table_elements:

        rows = []

        for row in table.find_all("tr"):

            cells = row.find_all(
                ["th", "td"]
            )

            row_data = []

            for cell in cells:

                # -----------------------------
                # Check if cell contains image
                # -----------------------------

                image = cell.find("img")

                if image and image.get("src"):

                    image_url = urljoin(
                        response.url,
                        image.get("src")
                    )

                    row_data.append(
                        f"Image: {image_url}"
                    )

                # -----------------------------
                # Check if cell contains link
                # -----------------------------

                elif cell.find("a"):

                    link = cell.find("a")

                    link_text = link.get_text(
                        " ",
                        strip=True
                    )

                    href = link.get("href")

                    if href:

                        link_url = urljoin(
                            response.url,
                            href
                        )

                        if link_text:

                            row_data.append(
                                f"{link_text} → {link_url}"
                            )

                        else:

                            row_data.append(
                                link_url
                            )

                    else:

                        row_data.append(
                            link_text
                        )

                # -----------------------------
                # Normal text cell
                # -----------------------------

                else:

                    text = cell.get_text(
                        " ",
                        strip=True
                    )

                    row_data.append(text)

            if row_data:

                rows.append(row_data)

        tables.append(rows)

    # -----------------------------
    # Return everything
    # -----------------------------

    return {
        "url": response.url,
        "status_code": response.status_code,
        "title": title,

        "headings": headings,
        "paragraphs": paragraphs,
        "links": links,
        "images": images,
    
        "tables": tables
    }


def get_links(url):

    result = analyze_page(url)

    return result["links"]