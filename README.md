# Facebook Post Comment Scraper

Tool Python dùng để crawl bài viết, bình luận, phản hồi bình luận và ảnh từ Facebook bằng HTTP requests/GraphQL, có giao diện PyQt6 để thao tác nhanh.

> Dự án phục vụ mục đích học tập, nghiên cứu dữ liệu và sử dụng nội bộ. Người dùng tự chịu trách nhiệm về việc tuân thủ điều khoản của Facebook/Meta và quy định pháp luật liên quan.

## Tính năng chính

- Crawl một hoặc nhiều bài viết Facebook.
- Crawl nhiều bài viết từ Page/Profile.
- Crawl nhiều bài viết từ Group.
- Lấy comment, reply comment, số reaction và một số metadata của bài viết.
- Tải ảnh từ bài viết khi tìm được `media_id`.
- Hỗ trợ cookie và `fb_dtsg` để dùng session đã đăng nhập.
- Hỗ trợ proxy qua file `.env`.
- Xuất dữ liệu gốc dạng JSON.
- Convert JSON đã crawl sang CSV bằng `export_json_to_csv.py`.

## Yêu cầu

- Python 3.8 trở lên.
- Cookie Facebook hợp lệ nếu cần crawl nội dung yêu cầu đăng nhập.
- Kết nối mạng ổn định.

## Cài đặt

```bash
pip install -r requirements.txt
```

Hoặc cài thủ công:

```bash
pip install requests PyQt6 python-dotenv seleniumbase
```

Tạo file `.env` ở thư mục gốc nếu cần dùng proxy:

```env
PROXY=http://username:password@proxy-server:port
```

## Chạy giao diện

```bash
python facebook_ui.py
```

Giao diện có 3 tab chính:

1. `Simple Post`: crawl comment/ảnh từ một hoặc nhiều URL bài viết.
2. `Page Posts`: crawl nhiều bài từ Page/Profile.
3. `Group Posts`: crawl nhiều bài từ Group.

Mỗi ô URL hỗ trợ nhiều dòng, mỗi dòng là một URL Facebook. Không dán cURL vào ô URL. Nếu cần dùng cookie/session, bấm `Configure Cookies & FB_DTSG`.

## Lấy cookie và fb_dtsg

Trong giao diện, bấm `Configure Cookies & FB_DTSG`, sau đó chọn một trong hai cách:

- Mở Chrome tự động, đăng nhập Facebook, rồi xác nhận để tool lấy cookie.
- Dán lệnh `Copy as cURL` từ request GraphQL trong DevTools Network để tool parse cookie và `fb_dtsg`.

Sau khi cấu hình xong, log sẽ hiển thị số cookie và token đã nhận.

## Cấu trúc dữ liệu xuất ra

Mặc định dữ liệu crawl được lưu thành JSON theo cấu trúc:

```text
simple_post/<post_id>/<post_id>.json
page_post/<page_name>/<post_id>/<post_id>.json
group_post/<group_name>/<post_id>/<post_id>.json
```

Ví dụ một file JSON:

```json
{
  "post_id": "123456789",
  "type": "simple_post",
  "post_info": {
    "post_story_id": "...",
    "media_id": "..."
  },
  "comments": [
    {
      "text": "Noi dung comment",
      "reaction_count": "0",
      "replies": []
    }
  ]
}
```

Ảnh, nếu tải được, sẽ nằm cùng thư mục với file JSON của bài viết.

## Convert JSON sang CSV

Script `export_json_to_csv.py` đọc toàn bộ file `.json` trong thư mục input và tạo 2 file:

- `posts.csv`: thông tin bài viết.
- `comments.csv`: comment và reply comment.

Lệnh cơ bản:

```bash
python export_json_to_csv.py --input simple_post --output csv_export/simple_post
```

Convert dữ liệu Page:

```bash
python export_json_to_csv.py --input page_post --output csv_export/page_post
```

Convert dữ liệu Group:

```bash
python export_json_to_csv.py --input group_post --output csv_export/group_post
```

Convert riêng một thư mục chiến dịch/từ khóa:

```bash
python export_json_to_csv.py --input "simple_post/mandalorian và grogu" --output "csv_export/mandalorian và grogu"
```

Sau khi chạy xong, kết quả sẽ có dạng:

```text
csv_export/<ten_thu_muc>/posts.csv
csv_export/<ten_thu_muc>/comments.csv
```

Các file CSV được ghi bằng encoding `utf-8-sig`, có thể mở trực tiếp bằng Excel.

### Cột trong posts.csv

- `post_id`
- `feedback_id`
- `page_name`
- `text`
- `permalink`
- `comment_count`
- `reaction_count`
- `share_count`
- `interaction_count`
- `media_count`
- `media_urls`
- `json_path`

### Cột trong comments.csv

- `post_id`
- `page_name`
- `comment_level`: `0` là comment gốc, `1` trở lên là reply.
- `comment_text`
- `reaction_count`
- `parent_comment_text`
- `json_path`

## Chạy bằng CLI

Repo vẫn có CLI trong `main.py`:

```bash
python main.py
```

Sau đó chọn loại crawl trong menu:

```text
1. Simple Post
2. Page Posts
3. Group Posts
4. Exit
```

Với nhu cầu sử dụng hằng ngày, nên dùng `facebook_ui.py` vì dễ nhập nhiều URL, cấu hình cookie và theo dõi log hơn.

## Cấu trúc project

```text
facebook_post_comment_scraper-main/
├── facebook_ui.py              # Giao diện PyQt6
├── main.py                     # CLI và hàm lưu dữ liệu
├── post_scraper.py             # Crawl bài từ Page/Profile
├── group_post_scraper_v2.py    # Crawl bài từ Group
├── comment_scraper.py          # Crawl comment/reply
├── single_post_image.py        # Tải ảnh bài viết
├── export_json_to_csv.py       # Convert JSON sang CSV
├── proxy_utils.py              # Chọn proxy
├── simple_post/                # Dữ liệu Simple Post
├── page_post/                  # Dữ liệu Page, nếu có
├── group_post/                 # Dữ liệu Group, nếu có
└── csv_export/                 # CSV sau khi convert
```

## Lỗi thường gặp

### GUI không mở

Kiểm tra PyQt6:

```bash
pip install --upgrade PyQt6
```

### Không lấy được dữ liệu

- Kiểm tra URL có đúng định dạng Facebook không.
- Kiểm tra nội dung có public hoặc session có quyền xem không.
- Cấu hình lại cookie và `fb_dtsg`.
- Kiểm tra proxy trong `.env`.

### Request lỗi nhiều lần

- Facebook có thể đã đổi GraphQL/doc id.
- Cookie/session có thể đã hết hạn.
- Proxy có thể chậm hoặc bị chặn.
- Nên giảm tốc độ crawl hoặc thử lại sau.

## Lưu ý

- Không crawl dữ liệu riêng tư nếu không có quyền.
- Không gửi request quá nhanh để tránh bị giới hạn.
- Không chia sẻ cookie hoặc file `.env`.
- Tool không liên kết và không được xác nhận bởi Facebook/Meta.
