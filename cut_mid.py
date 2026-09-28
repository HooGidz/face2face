import os
from moviepy import VideoFileClip, concatenate_videoclips
from datetime import datetime

def time_to_seconds(time_str):
    """
    Hàm chuyển đổi chuỗi thời gian "HH:MM:SS" hoặc "MM:SS" thành tổng số giây.
    Ví dụ: "00:13:45" -> 825 giây
    """
    parts = list(map(int, time_str.split(':')))
    if len(parts) == 3:
        # Định dạng HH:MM:SS
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    elif len(parts) == 2:
        # Định dạng MM:SS
        return parts[0] * 60 + parts[1]
    elif len(parts) == 1:
        # Nếu nhập trực tiếp số giây
        return parts[0]
    else:
        raise ValueError("Định dạng thời gian không hợp lệ!")

def cut_video_segment(input_path, output_path, thoi_diem_bat_dau, thoi_diem_ket_thuc):
    """
    Cắt bỏ khoảng thời gian từ thoi_diem_bat_dau đến thoi_diem_ket_thuc (dạng "HH:MM:SS")
    và ghép các phần còn lại.
    """
    if not os.path.exists(input_path):
        print(f"Lỗi: Không tìm thấy file video tại '{input_path}'")
        return

    # Chuyển đổi định dạng HH:MM:SS sang giây
    start_cut = time_to_seconds(thoi_diem_bat_dau)
    end_cut = time_to_seconds(thoi_diem_ket_thuc)

    print("Đang tải video...")
    video = VideoFileClip(input_path)
    total_duration = video.duration

    # Kiểm tra thời gian nhập vào có hợp lệ không
    if start_cut < 0 or end_cut > total_duration or start_cut >= end_cut:
        print(f"Lỗi: Thời gian cắt không hợp lệ!")
        print(f"Tổng thời lượng video là: {total_duration:.2f} giây")
        video.close()
        return

    print(f"Xóa đoạn từ {thoi_diem_bat_dau} ({start_cut}s) đến {thoi_diem_ket_thuc} ({end_cut}s)...")

    # Cắt phần 1: Từ đầu video đến thời điểm bắt đầu xóa
    clip1 = video.subclipped(0, start_cut)
    
    # Cắt phần 2: Từ thời điểm kết thúc xóa đến hết video
    clip2 = video.subclipped(end_cut, total_duration)

    # Ghép 2 đoạn lại
    final_clip = concatenate_videoclips([clip1, clip2])

    print("Đang xử lý và xuất video...")
    final_clip.write_videofile(
        output_path, 
        codec="libx264", 
        audio_codec="aac"
    )

    # Giải phóng bộ nhớ
    video.close()
    clip1.close()
    clip2.close()
    final_clip.close()
    print(f" Xử lý hoàn tất! File mới: {output_path}")

# --- CẤU HÌNH VÀ CHẠY ---
if __name__ == "__main__":
    file_goc = r"D:\BotEMA\Yua IS-338 (1440).mp4"       # Tên file video của bạn
    
    # Lấy đường dẫn thư mục và tên file gốc để tạo tên file đầu ra
    thu_muc_luu = os.path.dirname(file_goc)
    ten_file_goc = os.path.splitext(os.path.basename(file_goc))[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_ra = os.path.join(thu_muc_luu, f"{ten_file_goc}_cut_{timestamp}.mp4")
    
    # Nhập thời gian cắt dạng "HH:MM:SS" hoặc "MM:SS"
    thoi_diem_bat_dau = "02:21:25"   # Bắt đầu cắt từ giây 0
    thoi_diem_ket_thuc = "02:23:50"   # Cắt đến phút thứ 13, giây 45
    
    print(f"File đầu ra sẽ được lưu tại: {file_ra}")
    cut_video_segment(file_goc, file_ra, thoi_diem_bat_dau, thoi_diem_ket_thuc)