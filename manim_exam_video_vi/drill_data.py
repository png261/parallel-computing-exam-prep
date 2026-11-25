"""Cac bai drill tren man hinh (3 bai moi module). Sinh tu ngan hang cau hoi practice quiz."""

DRILLS = {
  "M1": [
    {
      "q": "Amdahl: 90% mã chạy song song. Speedup tối đa với số bộ xử lý vô hạn?",
      "opts": ["9x","10x","90x","Không giới hạn"],
      "ans": 1,
      "say_q": "Nếu chín mươi phần trăm chương trình có thể song song hóa, thì speedup tối đa với số bộ xử lý vô hạn là bao nhiêu?",
      "say_a": "Mười lần. Phần tuần tự mười phần trăm không bao giờ co lại, nên speedup bị chặn ở một chia không phẩy một, tức là mười."
    },
    {
      "q": "Mô hình PRAM nào hạn chế nhất, nên thuật toán của nó chạy được trên mọi mô hình khác?",
      "opts": ["CRCW","CREW","EREW","ERCW"],
      "ans": 2,
      "say_q": "Mô hình PRAM nào hạn chế nhất, để thuật toán của nó cũng chạy đúng trên tất cả các mô hình còn lại?",
      "say_a": "EREW, đọc độc quyền ghi độc quyền. Thuật toán EREW không bao giờ dựa vào truy cập đồng thời, nên chạy được cả trên CREW và CRCW, nhưng chiều ngược lại thì không."
    },
    {
      "q": "Isoefficiency: hệ X cần W = Θ(p log p), hệ Y cần W = Θ(p²). Hệ nào dễ mở rộng hơn?",
      "opts": ["X","Y","Mở rộng như nhau","Không thể biết"],
      "ans": 0,
      "say_q": "Hệ X có isoefficiency cỡ p log p, hệ Y có cỡ p bình phương. Hệ nào dễ mở rộng hơn?",
      "say_a": "Hệ X. Isoefficiency cho biết kích thước bài toán phải tăng nhanh đến đâu để giữ hiệu suất không đổi. Tăng chậm hơn, p log p thay vì p bình phương, nghĩa là hệ dễ mở rộng hơn."
    }
  ],
  "M2": [
    {
      "q": "OpenMP: mệnh đề nào khiến mỗi luồng cộng riêng rồi gộp một lần?",
      "opts": ["critical","reduction(+:sum)","atomic","firstprivate(sum)"],
      "ans": 1,
      "say_q": "Trong OpenMP, mệnh đề nào cho mỗi luồng một biến sum riêng và chỉ gộp chúng một lần ở cuối?",
      "say_a": "Reduction cộng sum. Mỗi luồng bắt đầu từ không và các tổng riêng được gộp một lần, nên nhanh hơn nhiều so với critical hay atomic vốn đồng bộ ở mỗi vòng lặp."
    },
    {
      "q": "Java: gọi wait() ngoài khối synchronized gây ra gì?",
      "opts": ["Deadlock","Không có gì xảy ra","IllegalMonitorStateException","Luồng bị chấm dứt"],
      "ans": 2,
      "say_q": "Trong Java, điều gì xảy ra nếu bạn gọi wait bên ngoài khối synchronized trên đối tượng đó?",
      "say_a": "Ngoại lệ IllegalMonitorStateException được ném ra. wait, notify và notifyAll phải được gọi khi đang giữ khóa của đối tượng, vì wait sẽ nhả khóa đó."
    },
    {
      "q": "1000 vòng lặp, 4 luồng, schedule(static): luồng 2 nhận những vòng lặp nào?",
      "opts": ["500 đến 749","250 đến 499","2, 6, 10, ...","750 đến 999"],
      "ans": 0,
      "say_q": "Một vòng lặp một nghìn lần chạy với schedule static trên bốn luồng. Luồng hai nhận những vòng lặp nào?",
      "say_a": "Các vòng lặp từ 500 đến 749. Static mặc định cho mỗi luồng một khối liên tục cỡ N chia p, tức là mỗi luồng 250 vòng lặp."
    }
  ],
  "M3": [
    {
      "q": "Cả hai rank gọi MPI_Send 1005 số int rồi mới MPI_Recv (ngưỡng eager 4096 B). Kết quả?",
      "opts": ["Chạy xong bình thường","Deadlock (rendezvous)","Lỗi: bộ đệm quá nhỏ","Thông điệp đến sai thứ tự"],
      "ans": 1,
      "say_q": "Hai rank cùng gọi MPI Send với một nghìn không trăm lẻ năm số nguyên trước khi nhận, với ngưỡng eager 4096 byte. Chuyện gì xảy ra?",
      "say_a": "Deadlock. Bốn nghìn không trăm hai mươi byte cộng phần header vượt ngưỡng eager, nên rendezvous khiến mỗi Send chờ một Recv không bao giờ bắt đầu. Sửa bằng MPI Sendrecv hoặc các lời gọi không chặn."
    },
    {
      "q": "4 rank giữ v = 1, 2, 3, 4. MPI_Scan với MPI_SUM: giá trị tại rank 3?",
      "opts": ["4","6","10","1"],
      "ans": 2,
      "say_q": "Bốn rank giữ các giá trị một, hai, ba và bốn. Sau MPI Scan bao gồm với phép cộng, rank ba giữ giá trị nào?",
      "say_a": "Mười. Scan là phép rút gọn tiền tố bao gồm, nên rank ba nhận một cộng hai cộng ba cộng bốn."
    },
    {
      "q": "Chế độ gửi nào âm thầm bỏ thông điệp nếu bên nhận chưa sẵn sàng?",
      "opts": ["Synchronous","Buffered","Standard","Ready"],
      "ans": 3,
      "say_q": "Theo bài giảng, chế độ gửi MPI nào âm thầm bỏ thông điệp nếu bên nhận chưa sẵn sàng?",
      "say_a": "Ready send. Nó hoàn tất ngay và chỉ hoạt động nếu lệnh nhận tương ứng đã được đăng ký sẵn; còn buffered send thì giữ dữ liệu trong bộ đệm của người dùng."
    }
  ],
  "M4": [
    {
      "q": "Một kernel CUDA __global__ bắt buộc có kiểu trả về nào?",
      "opts": ["int","void","float","Kiểu bất kỳ"],
      "ans": 1,
      "say_q": "Một kernel CUDA global bắt buộc phải có kiểu trả về nào?",
      "say_a": "Void. Kernel được CPU khởi chạy và chạy trên GPU, nên không thể trả về giá trị. Nó ghi kết quả vào bộ nhớ thiết bị, rồi host sao chép về bằng cudaMemcpy."
    },
    {
      "q": "Hai luồng ở các block KHÁC NHAU của cùng một grid cần đồng bộ. Điều nào đúng?",
      "opts": ["Dùng __syncthreads()","Dùng shared memory","Không thể đồng bộ đáng tin cậy","Quay vòng chờ trên khóa toàn cục"],
      "ans": 2,
      "say_q": "Hai luồng ở các block khác nhau của cùng một grid cần đồng bộ với nhau. Điều nào đúng?",
      "say_a": "Chúng không thể đồng bộ đáng tin cậy. Các block có thể chạy theo thứ tự bất kỳ, nên không đảm bảo cả hai cùng tồn tại một lúc. Hãy dùng một lần khởi chạy kernel mới làm rào chắn toàn cục."
    },
    {
      "q": "SAXPY với 256 luồng/block, n = 1000: có bao nhiêu block được khởi chạy?",
      "opts": ["3","5","1000","4"],
      "ans": 3,
      "say_q": "SAXPY dùng 256 luồng mỗi block và n bằng một nghìn. Có bao nhiêu block được khởi chạy?",
      "say_a": "Bốn. n cộng 255, chia cho 256, là 1255 chia 256, cắt phần nguyên được 4. Như vậy có 1024 luồng, và câu kiểm tra if i nhỏ hơn n làm 24 luồng cuối ở trạng thái rảnh."
    }
  ],
  "M5": [
    {
      "q": "Find-Max với accelerated cascading: (work, time) của nó là gì?",
      "opts": ["O(n), O(log log n)","O(n^2), O(1)","O(n log log n), O(log log n)","O(n), O(log n)"],
      "ans": 0,
      "say_q": "Dùng accelerated cascading, Find-Max song song đạt work và time bao nhiêu?",
      "say_a": "Work cỡ n và time cỡ log log n. Đầu tiên một cây cân bằng rút n xuống còn n chia log log n ứng viên với chi phí tuyến tính, rồi cây DLDT hoàn tất trong log log n bước."
    },
    {
      "q": "Mạng sắp xếp bitonic cho n = 16: có bao nhiêu cột comparator?",
      "opts": ["4","16","10","8"],
      "ans": 2,
      "say_q": "Mạng sắp xếp bitonic cần bao nhiêu cột comparator cho mười sáu phần tử?",
      "say_a": "Mười. Với log n bằng bốn, độ sâu là bốn nhân năm chia hai, bằng mười. Đó là cỡ log bình phương n."
    },
    {
      "q": "Sample sort trên p = 4 bộ xử lý: có bao nhiêu mẫu được sắp xếp để chọn các splitter?",
      "opts": ["12","16","3","4"],
      "ans": 0,
      "say_q": "Trong sample sort trên bốn bộ xử lý, có bao nhiêu mẫu được thu thập và sắp xếp để chọn các splitter toàn cục?",
      "say_a": "Mười hai. Mỗi bộ xử lý chọn p trừ một, tức là ba, mẫu cách đều, nên p nhân p trừ một là mười hai. Sau đó chọn p trừ một, tức là ba, splitter toàn cục."
    }
  ]
}


def drill_segments():
    segs = {}
    for mod, items in DRILLS.items():
        for i, it in enumerate(items, 1):
            segs[f"d{mod}_{i}_q"] = it["say_q"] + " Hãy đọc bốn đáp án, và tạm dừng video nếu cần thêm thời gian."
            segs[f"d{mod}_{i}_a"] = f"Đáp án là {'ABCD'[it['ans']]}. " + it["say_a"]
    return segs
