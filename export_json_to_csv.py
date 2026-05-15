import argparse
import csv
import json
from pathlib import Path


POST_FIELDS = [
    "post_id",
    "feedback_id",
    "page_name",
    "text",
    "permalink",
    "comment_count",
    "reaction_count",
    "share_count",
    "interaction_count",
    "media_count",
    "media_urls",
    "json_path",
]

COMMENT_FIELDS = [
    "post_id",
    "page_name",
    "comment_level",
    "comment_text",
    "reaction_count",
    "parent_comment_text",
    "json_path",
]


def read_json(path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def media_urls(post):
    urls = []
    for item in post.get("media") or []:
        if isinstance(item, dict) and item.get("url"):
            urls.append(item["url"])
    return urls


def post_row(post, json_path):
    urls = media_urls(post)
    return {
        "post_id": post.get("post_id", ""),
        "feedback_id": post.get("feedback_id", ""),
        "page_name": post.get("page_name", ""),
        "text": post.get("text", ""),
        "permalink": post.get("permalink", ""),
        "comment_count": post.get("comment_count", ""),
        "reaction_count": post.get("reaction_count", ""),
        "share_count": post.get("share_count", ""),
        "interaction_count": post.get("interaction_count", ""),
        "media_count": len(urls),
        "media_urls": "\n".join(urls),
        "json_path": str(json_path),
    }


def iter_comments(comments, post, json_path, level=0, parent_text=""):
    for comment in comments or []:
        if not isinstance(comment, dict):
            continue

        text = comment.get("text", "")
        yield {
            "post_id": post.get("post_id", ""),
            "page_name": post.get("page_name", ""),
            "comment_level": level,
            "comment_text": text,
            "reaction_count": comment.get("reaction_count", ""),
            "parent_comment_text": parent_text,
            "json_path": str(json_path),
        }

        yield from iter_comments(
            comment.get("replies") or [],
            post,
            json_path,
            level=level + 1,
            parent_text=text,
        )


def export_json_folder(input_dir, output_dir):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    json_files = sorted(input_dir.rglob("*.json"))
    posts = []
    comments = []

    for json_path in json_files:
        try:
            post = read_json(json_path)
        except Exception as exc:
            print(f"Skipping {json_path}: {exc}")
            continue

        if not isinstance(post, dict):
            continue

        posts.append(post_row(post, json_path))
        comments.extend(iter_comments(post.get("comments") or [], post, json_path))

    posts_csv = output_dir / "posts.csv"
    comments_csv = output_dir / "comments.csv"

    with posts_csv.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=POST_FIELDS)
        writer.writeheader()
        writer.writerows(posts)

    with comments_csv.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COMMENT_FIELDS)
        writer.writeheader()
        writer.writerows(comments)

    return posts_csv, comments_csv, len(posts), len(comments)


def main():
    parser = argparse.ArgumentParser(
        description="Export scraped Facebook JSON files to CSV without copying/downloading JPG files."
    )
    parser.add_argument("--input", default="page_post", help="Folder containing scraped JSON files")
    parser.add_argument("--output", default="csv_export", help="Folder where CSV files will be written")
    args = parser.parse_args()

    posts_csv, comments_csv, post_count, comment_count = export_json_folder(args.input, args.output)
    print(f"Exported {post_count} posts to {posts_csv}")
    print(f"Exported {comment_count} comments/replies to {comments_csv}")


if __name__ == "__main__":
    main()
