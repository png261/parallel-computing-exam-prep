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
      "q": "Amdahl: P = 0,90 và N = 10 bộ xử lý. Speedup xấp xỉ?",
      "opts": ["10","9","5,26","1,9"],
      "ans": 2,
      "say_q": "Theo định luật Amdahl, chín mươi phần trăm mã song song hóa được, chạy trên mười bộ xử lý. Speedup xấp xỉ bao nhiêu?",
      "say_a": "Khoảng năm phẩy hai sáu. Speedup bằng một chia, P chia N cộng S, tức là một chia không phẩy chín mươi trên mười cộng không phẩy một, bằng một chia không phẩy mười chín."
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
      "q": "Vòng lặp có tải đều giữa các lần lặp. Nên thử schedule nào trước?",
      "opts": ["dynamic,1","static","guided","runtime với 1 khúc"],
      "ans": 1,
      "say_q": "Vòng lặp OpenMP có tải đều giữa các lần lặp. Nên bắt đầu thử với schedule nào?",
      "say_a": "Static. Nó có chi phí điều phối thấp nhất, giữ được vector hóa và tính cục bộ dữ liệu. Với tải đều, dynamic một chậm hơn nhiều vì mỗi lần lặp là một lần xin việc."
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
      "q": "Theo mô hình t(n) = α + n/β, nên làm gì khi gửi nhiều dữ liệu nhỏ?",
      "opts": ["Gửi nhiều thông điệp nhỏ","Gộp thành ít thông điệp lớn","Luôn dùng MPI_Send chặn","Không có khác biệt"],
      "ans": 1,
      "say_q": "Theo mô hình chi phí t của n bằng alpha cộng n chia beta, khi cần gửi nhiều dữ liệu nhỏ thì nên làm gì?",
      "say_a": "Gộp thành ít thông điệp lớn. Mỗi thông điệp đều phải trả độ trễ alpha, nên gửi ít thông điệp lớn sẽ rẻ hơn nhiều thông điệp nhỏ."
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
      "say_a": "Chúng không thể đồng bộ đáng tin cậy. Các block có thể chạy theo thứ tự bất kỳ, nên không đảm bảo cả hai cùng tồn tại một lúc. Vì vậy các block phải độc lập với nhau."
    },
    {
      "q": "SAXPY với 256 luồng/block, n = 1000: có bao nhiêu block được khởi chạy?",
      "opts": ["3","5","1000","4"],
      "ans": 3,
      "say_q": "SAXPY dùng 256 luồng mỗi block và n bằng một nghìn. Có bao nhiêu block được khởi chạy?",
      "say_a": "Bốn. n cộng 255, chia cho 256, là 1255 chia 256, cắt phần nguyên được 4. Như vậy có 1024 luồng, và câu kiểm tra if i nhỏ hơn n làm 24 luồng cuối ở trạng thái rảnh."
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
