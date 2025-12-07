import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Cấu hình trang
st.set_page_config(
    page_title="KẾT QUẢ PHÂN TÍCH THỐNG KÊ TRONG KINH DOANH",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Tiêu đề chính
st.title("📊 KẾT QUẢ PHÂN TÍCH THỐNG KÊ TRONG KINH DOANH")
st.markdown("---")

# Sidebar - Upload file
st.sidebar.header("📁 Tải Lên File Excel")
uploaded_file = st.sidebar.file_uploader(
    "Chọn file Excel để phân tích",
    type=['xlsx', 'xls'],
    help="Hỗ trợ định dạng .xlsx và .xls"
)

if uploaded_file is not None:
    try:
        # Đọc file Excel
        @st.cache_data
        def load_excel(uploaded_file):
            df = pd.read_excel(uploaded_file)
            return df
        
        df = load_excel(uploaded_file)
        
        # Hiển thị thông tin cơ bản
        st.sidebar.success(f"✅ Đã tải file thành công!")
        st.sidebar.info(f"📏 Kích thước: {df.shape[0]} dòng × {df.shape[1]} cột")
        
        # Tùy chọn chọn sheet (nếu có nhiều sheet)
        if 'xlsx' in uploaded_file.name:
            try:
                excel_file = pd.ExcelFile(uploaded_file)
                if len(excel_file.sheet_names) > 1:
                    selected_sheet = st.sidebar.selectbox(
                        "Chọn sheet:",
                        excel_file.sheet_names
                    )
                    df = pd.read_excel(uploaded_file, sheet_name=selected_sheet)
            except:
                pass
        
        # Chọn cột để phân tích
        st.sidebar.markdown("---")
        st.sidebar.subheader("⚙️ Tùy Chọn Phân Tích")
        
        # Hiển thị dữ liệu thô
        st.header("📋 Xem Trước Dữ Liệu")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Tổng số dòng", df.shape[0])
        with col2:
            st.metric("Tổng số cột", df.shape[1])
        with col3:
            st.metric("Tổng số ô", df.shape[0] * df.shape[1])
        
        # Tùy chọn hiển thị
        show_data = st.checkbox("Hiển thị dữ liệu chi tiết", value=False)
        if show_data:
            st.dataframe(df, use_container_width=True, height=400)
        
        st.markdown("---")
        
        # Phân tích thống kê tổng hợp
        st.header("📊 Thống Kê Tổng Hợp")
        
        # Chọn các cột số để phân tích
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
        
        if len(numeric_columns) > 0:
            st.subheader("🔢 Thống Kê Mô Tả Cho Các Cột Số")
            
            # Tạo tabs cho các loại thống kê
            tab1, tab2, tab3 = st.tabs(["📈 Tổng Quan", "📋 Chi Tiết", "🔍 Phân Tích Từng Cột"])
            
            with tab1:
                st.dataframe(df[numeric_columns].describe(), use_container_width=True)
                
                # Hiển thị các metric tổng hợp
                st.markdown("### 💎 Các Chỉ Số Tổng Hợp")
                cols = st.columns(min(len(numeric_columns), 4))
                
                for idx, col in enumerate(numeric_columns):
                    with cols[idx % 4]:
                        total = df[col].sum()
                        mean = df[col].mean()
                        st.metric(
                            label=f"Tổng {col}",
                            value=f"{total:,.2f}",
                            delta=f"Trung bình: {mean:,.2f}"
                        )
            
            with tab2:
                st.markdown("### 📊 Bảng Thống Kê Chi Tiết")
                stats_data = []
                
                for col in numeric_columns:
                    stats_data.append({
                        'Cột': col,
                        'Tổng': df[col].sum(),
                        'Trung Bình': df[col].mean(),
                        'Trung Vị': df[col].median(),
                        'Độ Lệch Chuẩn': df[col].std(),
                        'Min': df[col].min(),
                        'Max': df[col].max(),
                        'Số Giá Trị Thiếu': df[col].isna().sum(),
                        'Số Giá Trị Khác 0': (df[col] != 0).sum()
                    })
                
                stats_df = pd.DataFrame(stats_data)
                st.dataframe(stats_df.style.format({
                    'Tổng': '{:,.2f}',
                    'Trung Bình': '{:,.2f}',
                    'Trung Vị': '{:,.2f}',
                    'Độ Lệch Chuẩn': '{:,.2f}',
                    'Min': '{:,.2f}',
                    'Max': '{:,.2f}'
                }), use_container_width=True)
            
            with tab3:
                selected_numeric = st.selectbox(
                    "Chọn cột số để phân tích chi tiết:",
                    numeric_columns,
                    key="numeric_detail"
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"### 📊 Thống Kê: {selected_numeric}")
                    detail_stats = {
                        'Số lượng': len(df[selected_numeric]),
                        'Tổng': df[selected_numeric].sum(),
                        'Trung bình': df[selected_numeric].mean(),
                        'Trung vị': df[selected_numeric].median(),
                        'Độ lệch chuẩn': df[selected_numeric].std(),
                        'Phương sai': df[selected_numeric].var(),
                        'Giá trị nhỏ nhất': df[selected_numeric].min(),
                        'Giá trị lớn nhất': df[selected_numeric].max(),
                        'Quartile 25%': df[selected_numeric].quantile(0.25),
                        'Quartile 75%': df[selected_numeric].quantile(0.75),
                        'Số giá trị thiếu': df[selected_numeric].isna().sum(),
                        'Số giá trị duy nhất': df[selected_numeric].nunique()
                    }
                    
                    for key, value in detail_stats.items():
                        if isinstance(value, (int, np.integer)):
                            st.write(f"**{key}:** {value:,}")
                        else:
                            st.write(f"**{key}:** {value:,.2f}")
                
                with col2:
                    st.markdown(f"### 📈 Phân Phối: {selected_numeric}")
                    fig_hist = px.histogram(
                        df,
                        x=selected_numeric,
                        nbins=30,
                        title=f"Histogram của {selected_numeric}",
                        color_discrete_sequence=px.colors.qualitative.Set3,
                        labels={selected_numeric: selected_numeric, 'count': 'Tần số'}
                    )
                    fig_hist.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(size=12)
                    )
                    st.plotly_chart(fig_hist, use_container_width=True)
        
        st.markdown("---")
        
        # Phần biểu đồ trực quan
        st.header("🎨 Biểu Đồ Trực Quan")
        
        # Chọn loại biểu đồ
        chart_type = st.selectbox(
            "Chọn loại biểu đồ:",
            [
                "Biểu đồ cột (Column Chart)",
                "Biểu đồ đường (Line Chart)",
                "Biểu đồ tròn (Pie Chart)",
                "Biểu đồ phân tán (Scatter Plot)",
                "Biểu đồ hộp (Box Plot)",
                "Heatmap tương quan",
                "Biểu đồ kết hợp (Combined)"
            ]
        )
        
        if chart_type == "Biểu đồ cột (Column Chart)" and len(numeric_columns) > 0:
            selected_cols = st.multiselect(
                "Chọn cột số để vẽ biểu đồ cột:",
                numeric_columns,
                default=numeric_columns[:min(3, len(numeric_columns))]
            )
            
            if len(selected_cols) > 0:
                if len(categorical_columns) > 0:
                    group_by = st.selectbox(
                        "Nhóm theo cột:",
                        ["Không nhóm"] + categorical_columns
                    )
                    
                    if group_by != "Không nhóm":
                        df_grouped = df.groupby(group_by)[selected_cols].sum().reset_index()
                        fig = px.bar(
                            df_grouped,
                            x=group_by,
                            y=selected_cols,
                            title="Biểu đồ cột có nhóm",
                            color_discrete_sequence=px.colors.qualitative.Vivid,
                            barmode='group'
                        )
                    else:
                        fig = px.bar(
                            df[selected_cols].sum().reset_index(),
                            x='index',
                            y=0,
                            title="Biểu đồ cột tổng hợp",
                            labels={'index': 'Cột', 0: 'Giá trị'},
                            color_discrete_sequence=px.colors.qualitative.Set3
                        )
                else:
                    fig = px.bar(
                        df[selected_cols].sum().reset_index(),
                        x='index',
                        y=0,
                        title="Biểu đồ cột tổng hợp",
                        labels={'index': 'Cột', 0: 'Giá trị'},
                        color_discrete_sequence=px.colors.qualitative.Pastel
                    )
                
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    height=500
                )
                st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Biểu đồ đường (Line Chart)" and len(numeric_columns) > 0:
            selected_cols = st.multiselect(
                "Chọn cột số để vẽ biểu đồ đường:",
                numeric_columns,
                default=numeric_columns[:min(3, len(numeric_columns))]
            )
            
            if len(selected_cols) > 0:
                fig = px.line(
                    df,
                    y=selected_cols,
                    title="Biểu đồ đường",
                    color_discrete_sequence=px.colors.qualitative.Dark2,
                    markers=True
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    height=500,
                    xaxis_title="Chỉ số dòng",
                    yaxis_title="Giá trị"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Biểu đồ tròn (Pie Chart)":
            if len(categorical_columns) > 0:
                pie_column = st.selectbox(
                    "Chọn cột phân loại:",
                    categorical_columns
                )
                
                if len(numeric_columns) > 0:
                    value_column = st.selectbox(
                        "Chọn cột giá trị:",
                        numeric_columns
                    )
                    
                    pie_data = df.groupby(pie_column)[value_column].sum().reset_index()
                    
                    fig = px.pie(
                        pie_data,
                        values=value_column,
                        names=pie_column,
                        title=f"Biểu đồ tròn: {pie_column}",
                        color_discrete_sequence=px.colors.sequential.Viridis
                    )
                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    fig.update_layout(
                        font=dict(size=12),
                        height=500
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    pie_counts = df[pie_column].value_counts()
                    fig = px.pie(
                        values=pie_counts.values,
                        names=pie_counts.index,
                        title=f"Biểu đồ tròn: {pie_column}",
                        color_discrete_sequence=px.colors.sequential.Plasma
                    )
                    fig.update_traces(textposition='inside', textinfo='percent+label')
                    fig.update_layout(font=dict(size=12), height=500)
                    st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Biểu đồ phân tán (Scatter Plot)" and len(numeric_columns) >= 2:
            x_col = st.selectbox("Chọn cột trục X:", numeric_columns)
            y_col = st.selectbox("Chọn cột trục Y:", numeric_columns, index=1 if len(numeric_columns) > 1 else 0)
            
            if len(categorical_columns) > 0:
                color_col = st.selectbox(
                    "Tô màu theo:",
                    ["Không"] + categorical_columns
                )
                
                if color_col != "Không":
                    fig = px.scatter(
                        df,
                        x=x_col,
                        y=y_col,
                        color=color_col,
                        title=f"Biểu đồ phân tán: {x_col} vs {y_col}",
                        color_discrete_sequence=px.colors.qualitative.Light24,
                        size_max=15
                    )
                else:
                    fig = px.scatter(
                        df,
                        x=x_col,
                        y=y_col,
                        title=f"Biểu đồ phân tán: {x_col} vs {y_col}",
                        color_discrete_sequence=['#FF6B6B']
                    )
            else:
                fig = px.scatter(
                    df,
                    x=x_col,
                    y=y_col,
                    title=f"Biểu đồ phân tán: {x_col} vs {y_col}",
                    color_discrete_sequence=['#FF6B6B']
                )
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(size=12),
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Biểu đồ hộp (Box Plot)" and len(numeric_columns) > 0:
            selected_cols = st.multiselect(
                "Chọn cột số để vẽ biểu đồ hộp:",
                numeric_columns,
                default=numeric_columns[:min(5, len(numeric_columns))]
            )
            
            if len(selected_cols) > 0:
                fig = px.box(
                    df,
                    y=selected_cols,
                    title="Biểu đồ hộp",
                    color_discrete_sequence=px.colors.qualitative.Bold
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    height=500
                )
                st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Heatmap tương quan" and len(numeric_columns) > 1:
            corr_matrix = df[numeric_columns].corr()
            
            fig = px.imshow(
                corr_matrix,
                text_auto=True,
                aspect="auto",
                title="Ma trận tương quan",
                color_continuous_scale=px.colors.sequential.RdBu_r,
                labels=dict(color="Tương quan")
            )
            fig.update_layout(
                font=dict(size=12),
                height=600,
                width=800
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Hiển thị bảng tương quan
            st.markdown("### 📊 Bảng Tương Quan Chi Tiết")
            st.dataframe(corr_matrix.style.background_gradient(cmap='RdBu_r', vmin=-1, vmax=1).format("{:.2f}"), use_container_width=True)
        
        elif chart_type == "Biểu đồ kết hợp (Combined)" and len(numeric_columns) >= 2:
            selected_cols = st.multiselect(
                "Chọn 2 cột để vẽ biểu đồ kết hợp:",
                numeric_columns,
                default=numeric_columns[:2] if len(numeric_columns) >= 2 else numeric_columns
            )
            
            if len(selected_cols) >= 2:
                fig = make_subplots(specs=[[{"secondary_y": True}]])
                
                fig.add_trace(
                    go.Bar(
                        x=df.index,
                        y=df[selected_cols[0]],
                        name=selected_cols[0],
                        marker_color='#FF6B6B',
                        opacity=0.7
                    ),
                    secondary_y=False,
                )
                
                fig.add_trace(
                    go.Scatter(
                        x=df.index,
                        y=df[selected_cols[1]],
                        name=selected_cols[1],
                        mode='lines+markers',
                        line=dict(color='#4ECDC4', width=3),
                        marker=dict(size=6)
                    ),
                    secondary_y=True,
                )
                
                fig.update_xaxes(title_text="Chỉ số dòng")
                fig.update_yaxes(title_text=selected_cols[0], secondary_y=False)
                fig.update_yaxes(title_text=selected_cols[1], secondary_y=True)
                
                fig.update_layout(
                    title_text=f"Biểu đồ kết hợp: {selected_cols[0]} & {selected_cols[1]}",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(size=12),
                    height=500,
                    showlegend=True
                )
                st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Tính toán tổng hợp nâng cao
        st.header("🧮 Tính Toán Tổng Hợp Nâng Cao")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 📊 Tổng hợp theo nhóm")
            if len(categorical_columns) > 0 and len(numeric_columns) > 0:
                group_col = st.selectbox(
                    "Nhóm theo:",
                    categorical_columns,
                    key="group_agg"
                )
                agg_col = st.selectbox(
                    "Tính toán trên:",
                    numeric_columns,
                    key="agg_col"
                )
                
                agg_func = st.selectbox(
                    "Hàm tổng hợp:",
                    ["Tổng", "Trung bình", "Tối đa", "Tối thiểu", "Số lượng"],
                    key="agg_func"
                )
                
                func_map = {
                    "Tổng": "sum",
                    "Trung bình": "mean",
                    "Tối đa": "max",
                    "Tối thiểu": "min",
                    "Số lượng": "count"
                }
                
                if st.button("Tính toán", key="calc_agg"):
                    grouped = df.groupby(group_col)[agg_col].agg(func_map[agg_func]).reset_index()
                    grouped.columns = [group_col, f"{agg_func} của {agg_col}"]
                    
                    st.dataframe(grouped, use_container_width=True)
                    
                    # Vẽ biểu đồ
                    fig = px.bar(
                        grouped,
                        x=group_col,
                        y=f"{agg_func} của {agg_col}",
                        title=f"{agg_func} của {agg_col} theo {group_col}",
                        color_discrete_sequence=px.colors.qualitative.Set3
                    )
                    fig.update_layout(
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(size=12),
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 📈 Phân tích xu hướng")
            if len(numeric_columns) > 0:
                trend_col = st.selectbox(
                    "Cột để phân tích:",
                    numeric_columns,
                    key="trend_col"
                )
                
                if st.button("Phân tích", key="calc_trend"):
                    st.write("**Thống kê xu hướng:**")
                    
                    diff = df[trend_col].diff()
                    st.write(f"- Thay đổi trung bình: {diff.mean():,.2f}")
                    st.write(f"- Tăng nhiều nhất: {diff.max():,.2f}")
                    st.write(f"- Giảm nhiều nhất: {diff.min():,.2f}")
                    
                    # Biểu đồ xu hướng
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=df.index,
                        y=df[trend_col],
                        mode='lines+markers',
                        name=trend_col,
                        line=dict(color='#FF6B6B', width=2),
                        marker=dict(size=4)
                    ))
                    fig.update_layout(
                        title=f"Xu hướng của {trend_col}",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(size=12),
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
        
        with col3:
            st.markdown("### 🔢 Thống kê so sánh")
            if len(numeric_columns) >= 2:
                compare_col1 = st.selectbox(
                    "Cột 1:",
                    numeric_columns,
                    key="compare1"
                )
                compare_col2 = st.selectbox(
                    "Cột 2:",
                    numeric_columns,
                    key="compare2"
                )
                
                if st.button("So sánh", key="calc_compare"):
                    col1_mean = df[compare_col1].mean()
                    col2_mean = df[compare_col2].mean()
                    
                    st.write(f"**{compare_col1}:**")
                    st.write(f"- Trung bình: {col1_mean:,.2f}")
                    st.write(f"- Tổng: {df[compare_col1].sum():,.2f}")
                    
                    st.write(f"**{compare_col2}:**")
                    st.write(f"- Trung bình: {col2_mean:,.2f}")
                    st.write(f"- Tổng: {df[compare_col2].sum():,.2f}")
                    
                    st.write(f"**Tỷ lệ:** {col1_mean/col2_mean:.2f}")
                    
                    # Biểu đồ so sánh
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=[compare_col1, compare_col2],
                        y=[df[compare_col1].sum(), df[compare_col2].sum()],
                        marker_color=['#FF6B6B', '#4ECDC4'],
                        text=[f"{df[compare_col1].sum():,.0f}", f"{df[compare_col2].sum():,.0f}"],
                        textposition='auto'
                    ))
                    fig.update_layout(
                        title="So sánh tổng giá trị",
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(size=12),
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
        
        # Footer
        st.markdown("---")
        st.markdown(
            """
            <div style='text-align: center; color: gray; padding: 20px;'>
                <p>📊 Ứng dụng được tạo bằng Streamlit | Phân tích dữ liệu Excel chuyên nghiệp</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    except Exception as e:
        st.error(f"❌ Lỗi khi đọc file: {str(e)}")
        st.info("Vui lòng kiểm tra lại file Excel của bạn.")

else:
    # Hướng dẫn khi chưa có file
    st.info("👆 Vui lòng tải lên file Excel từ sidebar để bắt đầu phân tích.")
    
    st.markdown("""
    ### 📖 Hướng Dẫn Sử Dụng:
    
    1. **Tải lên file**: Chọn file Excel (.xlsx hoặc .xls) từ sidebar bên trái
    2. **Xem dữ liệu**: Xem trước và kiểm tra dữ liệu đã tải
    3. **Thống kê**: Xem các thống kê tổng hợp cho các cột số
    4. **Biểu đồ**: Chọn và tạo các biểu đồ trực quan với màu sắc sinh động
    5. **Tính toán**: Sử dụng các công cụ tính toán tổng hợp nâng cao
    
    ### ✨ Tính Năng:
    - ✅ Đọc và xử lý file Excel
    - ✅ Thống kê mô tả chi tiết
    - ✅ Biểu đồ màu sắc sinh động (cột, đường, tròn, phân tán, hộp, heatmap)
    - ✅ Tính toán tổng hợp (tổng, trung bình, max, min, số lượng)
    - ✅ Phân tích xu hướng
    - ✅ So sánh dữ liệu
    - ✅ Giao diện đẹp và dễ sử dụng
    """)
    
    # Tạo dữ liệu mẫu để demo
    st.markdown("---")
    st.subheader("💡 Tạo Dữ Liệu Mẫu Để Thử Nghiệm")
    
    if st.button("Tạo file Excel mẫu"):
        # Tạo dữ liệu mẫu
        np.random.seed(42)
        n = 100
        
        sample_data = {
            'Mã sản phẩm': [f'SP{i:03d}' for i in range(1, n+1)],
            'Loại sản phẩm': np.random.choice(['A', 'B', 'C', 'D'], n),
            'Giá bán': np.random.uniform(10000, 500000, n),
            'Số lượng': np.random.randint(10, 1000, n),
            'Doanh thu': np.random.uniform(500000, 5000000, n),
            'Chi phí': np.random.uniform(200000, 3000000, n),
            'Lợi nhuận': np.random.uniform(-100000, 2000000, n),
            'Tháng': np.random.choice(['Tháng 1', 'Tháng 2', 'Tháng 3', 'Tháng 4'], n),
            'Khu vực': np.random.choice(['Miền Bắc', 'Miền Trung', 'Miền Nam'], n)
        }
        
        sample_df = pd.DataFrame(sample_data)
        
        # Tạo file Excel
        output = pd.ExcelWriter('sample_data.xlsx', engine='openpyxl')
        sample_df.to_excel(output, index=False, sheet_name='Dữ liệu mẫu')
        output.close()
        
        st.success("✅ Đã tạo file Excel mẫu: sample_data.xlsx")
        st.info("📁 Bây giờ bạn có thể tải lên file này để thử nghiệm ứng dụng!")
        st.dataframe(sample_df.head(10))

