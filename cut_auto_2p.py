import os
import subprocess
from datetime import datetime

from facefusion import vision

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


def split_video_into_segments(
    input_path, output_dir=r"D:\BotEMA", segment_time=None, num_segments=None
):
    """Chia video thành các đoạn nhỏ. Có thể chia theo độ dài cố định hoặc chia đều.

    Args:
        input_path (str): Đường dẫn đến file video gốc.
        output_dir (str, optional): Thư mục lưu các đoạn video đã cắt. Mặc định là D:\\BotEMA.
        segment_time (int, optional): Độ dài cố định của mỗi đoạn video (tính bằng giây).
                                      Nếu được cung cấp, sẽ ưu tiên chia theo độ dài này.
        num_segments (int, optional): Số lượng đoạn video muốn chia đều.
                                      Nếu được cung cấp và segment_time không có, sẽ tính toán
                                      độ dài mỗi đoạn để chia đều.

    Lưu ý:
    - Nếu cả segment_time và num_segments đều được cung cấp, segment_time sẽ được ưu tiên.
    - Nếu không có tham số nào được cung cấp, hoặc cả hai đều None, sẽ báo lỗi.
    - Mỗi file đầu ra được re-encode để đảm bảo không bị lỗi mất hình/mất tiếng ở
      đầu video do không dính keyframe.

    Returns:
    Mỗi file đầu ra được re-encode để đảm bảo không bị lỗi mất hình/mất tiếng ở
    đầu video do không dính keyframe.
    """
    if not os.path.exists(input_path):
        print(f"Lỗi: Không tìm thấy file nguồn tại {input_path}")
        return

    if segment_time is None and num_segments is None:
        print("Lỗi: Phải cung cấp 'segment_time' (độ dài cố định) hoặc 'num_segments' (số lượng đoạn).")
        return

    if segment_time is None and num_segments is not None:
        if num_segments <= 0:
            print("Lỗi: Số lượng đoạn video phải lớn hơn 0.")
            return
        video_duration = vision.detect_video_duration(input_path)
        if video_duration is None or video_duration <= 0:
            print(f"Lỗi: Không thể xác định thời lượng video hoặc thời lượng video bằng 0 tại {input_path}. Vui lòng kiểm tra lại file hoặc FFprobe.")
            return
        segment_time = video_duration / num_segments
        print(f"Tổng thời lượng video: {video_duration:.2f} giây. Chia thành {num_segments} đoạn, mỗi đoạn {segment_time:.2f} giây.")

    if segment_time <= 0:
        print("Lỗi: Thời lượng mỗi đoạn video phải lớn hơn 0.")
        return

    # Tạo thư mục đầu ra nếu chưa có
    os.makedirs(output_dir, exist_ok=True)

    # Lấy tên file gốc (không bao gồm phần mở rộng) và timestamp để tránh trùng tên
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Mẫu tên file đầu ra: tên_goc_timestamp_part001.mp4, part002.mp4,...
    output_pattern = os.path.join(
        output_dir, f"{base_name}_{timestamp}_part-%03d.mp4"
    )

    command = [
        "ffmpeg",
        "-y",
        "-i",
        input_path,
        "-f",
        "segment",
        "-segment_time",
        str(segment_time),
        "-reset_timestamps",
        "1",
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "18",
        "-c:a",
        "aac",
        "-movflags",
        "+faststart",
        output_pattern,
    ]

    print(
        f"Đang tiến hành tự động chia nhỏ video thành các đoạn {segment_time} giây..."
    )
    if run_ffmpeg(command):
        print("--- THÀNH CÔNG! ---")
        print(f"Các video ngắn đã được lưu vào thư mục: {output_dir}")


# --- CẤU HÌNH Ở ĐÂY ---
file_goc = r"D:\BotEMA\output\pred-756.mp4"# Đường dẫn đến video gốc
thu_muc_luu = r"D:\BotEMA\output"  # Thư mục lưu các đoạn video đã cắt

# Cấu hình chia video:
# - Để chia theo độ dài cố định: bỏ comment dòng 'do_dai_moi_doan_giay' và giữ nguyên 'so_luong_doan_video = None'
# - Để chia đều theo số lượng đoạn: bỏ comment dòng 'so_luong_doan_video' và giữ nguyên 'do_dai_moi_doan_giay = None'

do_dai_moi_doan_giay = None  # Độ dài cố định của mỗi đoạn video (tính bằng giây). Ví dụ: 120 (2 phút)
so_luong_doan_video = 2     # Số lượng đoạn video muốn chia đều. Ví dụ: 5

# Chạy chức năng tự động chia nhỏ
split_video_into_segments(
    file_goc, output_dir=thu_muc_luu, segment_time=do_dai_moi_doan_giay, num_segments=so_luong_doan_video
)