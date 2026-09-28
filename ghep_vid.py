import os
import subprocess
from datetime import datetime


def run_ffmpeg(command):
    try:
        subprocess.run(command, check=True)
        return True
    except FileNotFoundError:
        print("Lỗi: Máy bạn chưa cài đặt FFmpeg hoặc chưa thêm vào PATH.")
        return False
    except subprocess.CalledProcessError as e:
        print(f"Lỗi khi thực hiện lệnh FFmpeg: {e}")
        return False


def merge_specific_videos(video_paths, output_file):
    """
    Ghép các file video được chỉ định thủ công trong danh sách video_paths.
    """
    if not video_paths:
        print("Lỗi: Danh sách video trống!")
        return

    # Kiểm tra xem tất cả các file nhập vào có tồn tại không
    missing_files = [path for path in video_paths if not os.path.exists(path)]
    if missing_files:
        print("Lỗi: Không tìm thấy các file sau:")
        for path in missing_files:
            print(f" - {path}")
        return

    # Tạo thư mục chứa file đầu ra nếu chưa có
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    print(f"Bắt đầu ghép {len(video_paths)} video theo danh sách bạn đã nhập...")

    # Chuẩn hóa timestamp và audio trước khi nối. Các đoạn có thể dùng codec
    # khác nhau (ví dụ AAC/FLAC), nên concat demuxer với -c copy sẽ làm mất tiếng.
    filter_parts = []
    concat_inputs = []
    for index in range(len(video_paths)):
        filter_parts.extend([
            f'[{index}:v:0]setpts=PTS-STARTPTS[v{index}]',
            f'[{index}:a:0]aresample=async=1:first_pts=0[a{index}]',
        ])
        concat_inputs.extend([f'[v{index}]', f'[a{index}]'])

    filter_parts.append(
        ''.join(concat_inputs)
        + f'concat=n={len(video_paths)}:v=1:a=1[outv][outa]'
    )

    command = ['ffmpeg', '-y']
    for path in video_paths:
        command.extend(['-i', path])
    command.extend([
        '-filter_complex', ';'.join(filter_parts),
        '-map', '[outv]',
        '-map', '[outa]',
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '18',
        '-pix_fmt', 'yuv420p',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-ar', '48000',
        '-ac', '2',
        '-movflags', '+faststart',
        output_file,
    ])

    success = run_ffmpeg(command)

    if success:
        print("--- THÀNH CÔNG! ---")
        print(f"Video ghép hoàn chỉnh đã lưu tại: {os.path.abspath(output_file)}")


# ==========================================
# --- KHU VỰC NHẬP ĐƯỜNG DẪN BẰNG TAY ---
# ==========================================
# Điền các đường dẫn video theo đúng thứ tự bạn muốn ghép vào đây:
danh_sach_video = [
    r"D:\BotEMA\output\b38eafc5.mp4",
    r"D:\BotEMA\output_cut_20260925_203437.mp4",



    # Bạn có thể thêm bao nhiêu video tùy thích, nhớ có dấu phẩy ở cuối mỗi dòng:
    # r"D:\BotEMA\doan_video_khac.mp4",
]

# Nơi lưu video thành phẩm
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
file_thanh_pham = rf"D:\BotEMA\ghep_video_{timestamp}.mp4"

# Thực thi ghép video
merge_specific_videos(danh_sach_video, file_thanh_pham)