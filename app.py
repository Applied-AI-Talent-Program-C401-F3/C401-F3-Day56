import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Import the pre-configured graph from agent
from agent import graph

# Cấu hình giao diện Streamlit
st.set_page_config(
    page_title="Vinmec Health Assistant", 
    page_icon="🏥", 
    layout="centered"
)

st.title("🏥 Hỗ trợ y tế Vinmec")
st.markdown("Hệ thống trợ lý ảo hỗ trợ tìm kiếm bác sĩ, kiểm tra lịch trống và đặt lịch khám.")

def get_message_text(content):
    if isinstance(content, str):
        return content
    elif isinstance(content, list):
        return "\n".join([item["text"] for item in content if isinstance(item, dict) and item.get("type") == "text"])
    return str(content)

# Khởi tạo lịch sử chat trong session_state nếu chưa có
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# Hiển thị các tin nhắn cũ từ lịch sử
for message in st.session_state.conversation_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage) and message.content:
        # Chỉ hiển thị các tin nhắn của Agent có chứa text (bỏ qua các tool_calls ẩn)
        text_content = get_message_text(message.content)
        if text_content:
            with st.chat_message("assistant"):
                st.markdown(text_content)

# Ô nhập tin nhắn từ người dùng
if prompt := st.chat_input("Nhập câu hỏi hoặc yêu cầu đặt lịch của bạn..."):
    
    # 1. Hiển thị tin nhắn người dùng ngay lập tức
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 2. Thêm vào lịch sử
    st.session_state.conversation_history.append(HumanMessage(content=prompt))
    
    # Lấy tối đa 10 tin nhắn gần nhất để tránh vượt quá context window
    graph_input_messages = st.session_state.conversation_history[-10:]

    # 3. Chạy qua LangGraph agent và chờ phản hồi
    with st.chat_message("assistant"):
        with st.spinner("Assistant đang xử lý..."):
            try:
                # Gọi agent. graph.invoke sẽ chạy luồng xử lý và tool calls (nếu có)
                result = graph.invoke({"messages": graph_input_messages})
                
                final_message = result["messages"][-1]
                response_content = get_message_text(final_message.content)
                
                # Hiển thị kết quả cho người dùng
                if response_content:
                    st.markdown(response_content)
                
                # Cập nhật lại lịch sử (lọc bỏ SystemMessage)
                updated_history = [
                    msg for msg in result["messages"] 
                    if not isinstance(msg, SystemMessage)
                ]
                st.session_state.conversation_history = updated_history
                
            except Exception as e:
                st.error(f"Đã có lỗi xảy ra trong quá trình xử lý: {str(e)}")
