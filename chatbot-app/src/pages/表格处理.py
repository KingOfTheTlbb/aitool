import streamlit as st
import pandas as pd
import io
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import zipfile
import os
from io import BytesIO
import pdfplumber
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
import matplotlib.font_manager as fm

# Language dictionary
LANGUAGES = {
    'en': {
        'app_title': 'Smart Excel Data Processing Tool',
        'data_transformation': '🔄 Data Transformation',
        'format_conversion': '📁 Format Conversion',
        'data_concat': '📈 Data Concatenation',
        'data_join': '🔗 Data Joining',
        'sheet_merge': '📑 Sheet Merging',
        'sheet_split': '✂️ Sheet Splitting',
        'excel_to_csv': '🔄 Excel to CSV',
        'csv_to_excel': '📂 CSV to Excel',
        'excel_to_pdf': '📄 Excel to PDF',
        'pdf_to_excel': '🔍 PDF to Excel',
        'main_header': '🛠️ Function Area',
        'data_concat_header': '📈 Data Concatenation (Data Concatenator)',
        'data_concat_desc': '''
        **Purpose**: Vertically stack and merge data tables with the same structure from multiple Excel files

        **Process**:
        1. Upload multiple Excel files
        2. System automatically analyzes the data structure of each sheet
        3. Vertically concatenate sheets with consistent structure
        4. Export the merged Excel file

        **Application Scenario**: Consolidate multiple monthly/quarterly reports with the same format
        ''',
        'select_files_concat': 'Select multiple Excel files for data concatenation',
        'file_info': 'File Information',
        'files_selected': 'files selected',
        'structure_check': 'Structure Consistency Check',
        'structure_consistent': '✅ All sheets have consistent data structure',
        'structure_inconsistent': '⚠️ Inconsistent sheets found:',
        'only_consistent': 'Only sheets with consistent structure will be concatenated',
        'output_filename': 'Output filename',
        'execute_concat': 'Execute Concatenation',
        'download_result': '📥 Download Result',
        'preview_result': 'Result Preview',
        'success_concat': '✅ Successfully concatenated {} data tables',
        'success_concat_consistent': '✅ Successfully concatenated {} data tables with consistent structure',
        'no_consistent_tables': '❌ No data tables with consistent structure found for concatenation',
        'reset_operation': '🔄 Reset Operation',
        'processing_concat': 'Concatenating data...',
        'error_processing': 'An error occurred during file processing: {}',
        'data_join_header': '🔗 Multi-table Key Field Association (Data Joiner)',
        'data_join_desc': '''
        **Purpose**: Merge multiple data tables by specifying key fields

        **Process**:
        1. Upload multiple Excel files
        2. System analyzes fields in all sheets
        3. Select key fields for association
        4. Select association method (Left join, Inner join, Outer join)
        5. Export the associated Excel file

        **Application Scenario**: Integrate multiple data sources with common identifier fields
        ''',
        'select_files_join': 'Select multiple Excel files for data association',
        'key_field_selection': 'Association Settings',
        'select_key_field': 'Select key field',
        'select_join_method': 'Select association method',
        'left_join': 'Left Join',
        'inner_join': 'Inner Join',
        'outer_join': 'Outer Join',
        'execute_join': 'Execute Association',
        'processing_join': 'Associating data...',
        'key_missing': "⚠️ Key field '{}' does not exist in some data tables, these tables will be skipped",
        'join_success_records': 'Successfully associated records: {}',
        'join_success': '✅ Data association completed',
        'no_valid_tables': '❌ Not enough valid data tables for association',
        'no_valid_tables_found': '❌ No valid data tables found',
        'sheet_merge_header': '📑 Multi-file Sheet Merging (Sheet Merger)',
        'sheet_merge_desc': '''
        **Purpose**: Merge all sheets from multiple Excel files into a new workbook

        **Process**:
        1. Upload multiple Excel files
        2. System automatically copies all sheets from each file
        3. Handle duplicate sheet names (automatically add serial number suffix)
        4. Export the merged Excel file

        **Application Scenario**: Integrate multiple worksheets scattered across different files
        ''',
        'select_files_merge': 'Select multiple Excel files for sheet merging',
        'execute_merge': 'Execute Merging',
        'processing_merge': 'Merging sheets...',
        'success_merge': '✅ Successfully merged {} files, totaling {} sheets',
        'sheet_split_header': '✂️ Single File Sheet Splitting (Sheet Splitter)',
        'sheet_split_desc': '''
        **Purpose**: Split each sheet in a single Excel file into independent Excel files

        **Process**:
        1. Upload an Excel file containing multiple sheets
        2. System automatically identifies all sheets
        3. Export each sheet as an independent Excel file
        4. Package as a ZIP file for download

        **Application Scenario**: Split comprehensive reports into separate worksheet files
        ''',
        'select_file_split': 'Select an Excel file for sheet splitting',
        'file_name': 'Filename',
        'sheet_count': 'Sheet Count',
        'sheet_list': 'Sheet List',
        'execute_split': 'Execute Splitting',
        'processing_split': 'Splitting sheets...',
        'download_split_result': '📥 Download Split Results (ZIP)',
        'success_split': '✅ Successfully split {} sheets',
        'split_sheets': 'Split Sheets:',
        'excel_to_csv_header': '🔄 Excel to CSV File (Excel to CSV Converter)',
        'excel_to_csv_desc': '''
        **Purpose**: Batch convert Excel files to CSV format files

        **Process**:
        1. Upload one or more Excel files
        2. System automatically reads all sheets from each file
        3. Convert each sheet to an independent CSV file
        4. Package all CSV files in ZIP format for download

        **Application Scenario**: Data format conversion for import into other systems
        ''',
        'select_excel_files': 'Select Excel files for conversion',
        'execute_conversion': 'Execute Conversion',
        'processing_excel_csv': 'Converting Excel files to CSV...',
        'download_csv_zip': '📥 Download CSV Files (ZIP)',
        'success_excel_csv': '✅ Successfully converted {} Excel files',
        'csv_to_excel_header': '📂 CSV to Excel File (CSV to Excel Converter)',
        'csv_to_excel_desc': '''
        **Purpose**: Batch convert CSV files to Excel format files

        **Process**:
        1. Upload one or more CSV files
        2. System automatically reads each CSV file
        3. Convert each CSV file to an independent Excel file
        4. Package all Excel files in ZIP format for download

        **Application Scenario**: Data format conversion for data analysis and processing
        ''',
        'select_csv_files': 'Select CSV files for conversion',
        'processing_csv_excel': 'Converting CSV files to Excel...',
        'download_excel_zip': '📥 Download Excel Files (ZIP)',
        'success_csv_excel': '✅ Successfully converted {} CSV files',
        'excel_to_pdf_header': '📄 Excel to PDF File (Excel to PDF Converter)',
        'excel_to_pdf_desc': '''
        **Purpose**: Batch convert Excel files to PDF format files

        **Process**:
        1. Upload one or more Excel files
        2. System automatically reads all sheets from each file
        3. Convert each sheet to an independent PDF file
        4. Package all PDF files in ZIP format for download

        **Application Scenario**: Document archiving, report sharing, print preview
        ''',
        'processing_excel_pdf': 'Converting Excel files to PDF...',
        'download_pdf_zip': '📥 Download PDF Files (ZIP)',
        'success_excel_pdf': '✅ Successfully converted {} Excel files',
        'pdf_to_excel_header': '🔍 PDF to Excel File (PDF to Excel Converter)',
        'pdf_to_excel_desc': '''
        **Purpose**: Extract table data from PDF files and convert to Excel format files

        **Process**:
        1. Upload one or more PDF files
        2. System automatically identifies and extracts all tables from the PDF
        3. Convert extracted table data to Excel files
        4. Package all Excel files in ZIP format for download

        **Application Scenario**: Data extraction, report conversion, document digitization
        ''',
        'select_pdf_files': 'Select PDF files for conversion',
        'processing_pdf_excel': 'Extracting tables from PDF files and converting to Excel...',
        'success_pdf_excel': '✅ Successfully processed {} PDF files',
        'footer': 'Smart Excel Data Processing Tool - Making Excel data processing easier',
        'language_toggle': '🌐 Language'
    },
    'zh': {
        'app_title': 'Smart Excel 数据处理工具',
        'data_transformation': '🔄 数据转换功能',
        'format_conversion': '📁 格式转换功能',
        'data_concat': '📈 数据拼接',
        'data_join': '🔗 数据关联',
        'sheet_merge': '📑 Sheet合并',
        'sheet_split': '✂️ Sheet拆分',
        'excel_to_csv': '🔄 Excel转CSV',
        'csv_to_excel': '📂 CSV转Excel',
        'excel_to_pdf': '📄 Excel转PDF',
        'pdf_to_excel': '🔍 PDF转Excel',
        'main_header': '🛠️ 功能操作区',
        'data_concat_header': '📈 多文件数据表拼接（Data Concatenator）',
        'data_concat_desc': '''
        **用途**：将多个Excel文件中结构相同的数据表垂直堆叠合并

        **操作流程**：
        1. 上传多个Excel文件
        2. 系统自动分析各Sheet的数据结构
        3. 将结构一致的Sheet数据垂直拼接
        4. 导出合并后的Excel文件

        **适用场景**：汇总多个格式相同的月度/季度报表
        ''',
        'select_files_concat': '选择多个Excel文件进行数据拼接',
        'file_info': '文件信息',
        'files_selected': '个文件',
        'structure_check': '结构一致性检查',
        'structure_consistent': '✅ 所有Sheet的数据结构一致',
        'structure_inconsistent': '⚠️ 发现结构不一致的Sheet:',
        'only_consistent': '只有结构一致的Sheet会被拼接',
        'output_filename': '输出文件名',
        'execute_concat': '执行拼接',
        'download_result': '📥 下载拼接结果',
        'preview_result': '结果预览',
        'success_concat': '✅ 成功拼接 {} 个数据表',
        'success_concat_consistent': '✅ 成功拼接 {} 个结构一致的数据表',
        'no_consistent_tables': '❌ 没有找到结构一致的数据表用于拼接',
        'reset_operation': '🔄 重置操作',
        'processing_concat': '正在拼接数据...',
        'error_processing': '文件处理过程中发生错误: {}',
        'data_join_header': '🔗 多表关键字段关联（Data Joiner）',
        'data_join_desc': '''
        **用途**：通过指定的关键字段将多个数据表关联合并

        **操作流程**：
        1. 上传多个Excel文件
        2. 系统分析所有Sheet中的字段
        3. 选择用于关联的关键字段
        4. 选择关联方式（左连接、内连接、外连接）
        5. 导出关联后的Excel文件

        **适用场景**：整合具有共同标识字段的多个数据源
        ''',
        'select_files_join': '选择多个Excel文件进行数据关联',
        'key_field_selection': '关联设置',
        'select_key_field': '选择关键字段',
        'select_join_method': '选择关联方式',
        'left_join': '左连接',
        'inner_join': '内连接',
        'outer_join': '外连接',
        'execute_join': '执行关联',
        'processing_join': '正在进行数据关联...',
        'key_missing': "⚠️ 关键字段 '{}' 在某些数据表中不存在，将跳过这些表",
        'join_success_records': '关联成功记录数: {}',
        'join_success': '✅ 数据关联完成',
        'no_valid_tables': '❌ 没有足够的有效数据表进行关联',
        'no_valid_tables_found': '❌ 未找到有效的数据表',
        'sheet_merge_header': '📑 多文件Sheet合并（Sheet Merger）',
        'sheet_merge_desc': '''
        **用途**：将多个Excel文件中的所有Sheet合并到一个新的工作簿中

        **操作流程**：
        1. 上传多个Excel文件
        2. 系统自动复制每个文件的所有Sheet
        3. 处理重名Sheet（自动添加序号后缀）
        4. 导出合并后的Excel文件

        **适用场景**：整合分散在不同文件中的多个工作表
        ''',
        'select_files_merge': '选择多个Excel文件进行Sheet合并',
        'execute_merge': '执行合并',
        'processing_merge': '正在合并Sheet...',
        'success_merge': '✅ 成功合并了 {} 个文件，共计 {} 个Sheet',
        'sheet_split_header': '✂️ 单文件Sheet拆分（Sheet Splitter）',
        'sheet_split_desc': '''
        **用途**：将单个Excel文件中的每个Sheet拆分为独立的Excel文件

        **操作流程**：
        1. 上传一个包含多个Sheet的Excel文件
        2. 系统自动识别所有Sheet
        3. 将每个Sheet导出为独立的Excel文件
        4. 打包为ZIP文件供下载

        **适用场景**：将综合报表拆分为单独的工作表文件
        ''',
        'select_file_split': '选择一个Excel文件进行Sheet拆分',
        'file_name': '文件名',
        'sheet_count': 'Sheet数量',
        'sheet_list': 'Sheet列表',
        'execute_split': '执行拆分',
        'processing_split': '正在拆分Sheet...',
        'download_split_result': '📥 下载拆分结果（ZIP）',
        'success_split': '✅ 成功拆分 {} 个Sheet',
        'split_sheets': '拆分的Sheet:',
        'excel_to_csv_header': '🔄 Excel转CSV文件（Excel to CSV Converter）',
        'excel_to_csv_desc': '''
        **用途**：将Excel文件批量转换为CSV格式文件

        **操作流程**：
        1. 上传一个或多个Excel文件
        2. 系统自动读取每个文件的所有Sheet
        3. 将每个Sheet转换为独立的CSV文件
        4. 打包所有CSV文件为ZIP格式供下载

        **适用场景**：数据格式转换，便于其他系统导入
        ''',
        'select_excel_files': '选择Excel文件进行转换',
        'execute_conversion': '执行转换',
        'processing_excel_csv': '正在转换Excel文件为CSV...',
        'download_csv_zip': '📥 下载CSV文件（ZIP）',
        'success_excel_csv': '✅ 成功转换 {} 个Excel文件',
        'csv_to_excel_header': '📂 CSV转Excel文件（CSV to Excel Converter）',
        'csv_to_excel_desc': '''
        **用途**：将CSV文件批量转换为Excel格式文件

        **操作流程**：
        1. 上传一个或多个CSV文件
        2. 系统自动读取每个CSV文件
        3. 将每个CSV文件转换为独立的Excel文件
        4. 打包所有Excel文件为ZIP格式供下载

        **适用场景**：数据格式转换，便于数据分析和处理
        ''',
        'select_csv_files': '选择CSV文件进行转换',
        'processing_csv_excel': '正在转换CSV文件为Excel...',
        'download_excel_zip': '📥 下载Excel文件（ZIP）',
        'success_csv_excel': '✅ 成功转换 {} 个CSV文件',
        'excel_to_pdf_header': '📄 Excel转PDF文件（Excel to PDF Converter）',
        'excel_to_pdf_desc': '''
        **用途**：将Excel文件批量转换为PDF格式文件

        **操作流程**：
        1. 上传一个或多个Excel文件
        2. 系统自动读取每个文件的所有Sheet
        3. 将每个Sheet转换为独立的PDF文件
        4. 打包所有PDF文件为ZIP格式供下载

        **适用场景**：文档归档、报告分享、打印预览
        ''',
        'processing_excel_pdf': '正在转换Excel文件为PDF...',
        'download_pdf_zip': '📥 下载PDF文件（ZIP）',
        'success_excel_pdf': '✅ 成功转换 {} 个Excel文件',
        'pdf_to_excel_header': '🔍 PDF转Excel文件（PDF to Excel Converter）',
        'pdf_to_excel_desc': '''
        **用途**：从PDF文件中提取表格数据并转换为Excel格式文件

        **操作流程**：
        1. 上传一个或多个PDF文件
        2. 系统自动识别并提取PDF中的所有表格
        3. 将提取的表格数据转换为Excel文件
        4. 打包所有Excel文件为ZIP格式供下载

        **适用场景**：数据提取、报表转换、文档数字化
        ''',
        'select_pdf_files': '选择PDF文件进行转换',
        'processing_pdf_excel': '正在从PDF文件提取表格并转换为Excel...',
        'success_pdf_excel': '✅ 成功处理 {} 个PDF文件',
        'footer': 'Smart Excel 数据处理工具 - 让Excel数据处理更简单',
        'language_toggle': '🌐 语言'
    }
}


# Function to get translated text
def _(key):
    lang = st.session_state.get('language', 'zh')  # Default to Chinese
    return LANGUAGES[lang].get(key, key)


# Set page configuration
st.set_page_config(
    page_title=_("app_title"),
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern, clean styling
st.markdown("""
<style>
    /* Modern color palette */
    :root {
        --primary-color: #4361ee;
        --secondary-color: #3f37c9;
        --accent-color: #4895ef;
        --success-color: #4cc9f0;
        --warning-color: #f72585;
        --light-bg: #f8f9fa;
        --dark-text: #212529;
        --light-text: #f8f9fa;
        --border-color: #dee2e6;
        --shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        --transition: all 0.3s ease;
    }

    /* Overall app styling */
    body {
        background-color: var(--light-bg);
        color: var(--dark-text);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Sidebar styling */
    [data-testid=stSidebar] {
        background: linear-gradient(180deg, #ffffff 0%, #f0f2f6 100%);
        border-right: 1px solid var(--border-color);
        padding-top: 20px;
    }

    /* Sidebar headers */
    .sidebar-header {
        color: var(--primary-color);
        font-size: 16px;
        font-weight: 600;
        padding: 12px 15px;
        margin: 0 10px 10px;
        border-bottom: 2px solid var(--accent-color);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Function buttons */
    .function-btn {
        padding: 14px 20px;
        margin: 8px 10px;
        border-radius: 10px;
        cursor: pointer;
        transition: var(--transition);
        font-weight: 500;
        text-align: left;
        width: calc(100% - 20px);
        border: none;
        background-color: white;
        color: var(--dark-text);
        box-shadow: var(--shadow);
        display: flex;
        align-items: center;
        font-size: 15px;
    }

    .function-btn:hover {
        background-color: var(--primary-color);
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(67, 97, 238, 0.2);
    }

    .function-btn.selected {
        background: linear-gradient(90deg, var(--primary-color) 0%, var(--secondary-color) 100%);
        color: white;
        font-weight: 600;
        box-shadow: 0 6px 12px rgba(67, 97, 238, 0.3);
    }

    /* Main header */
    .main-header {
        color: var(--primary-color);
        border-bottom: 3px solid var(--accent-color);
        padding-bottom: 15px;
        margin-bottom: 25px;
        font-size: 28px;
        font-weight: 700;
    }

    /* Function card container */
    .function-card {
        border-radius: 15px;
        padding: 30px;
        margin-bottom: 30px;
        box-shadow: var(--shadow);
        background: linear-gradient(180deg, #ffffff 0%, #fafafa 100%);
        border: 1px solid var(--border-color);
    }

    /* Expanders */
    .stExpander {
        border: 1px solid var(--border-color);
        border-radius: 10px;
        overflow: hidden;
        margin-bottom: 20px;
    }

    .stExpander > div:first-child {
        background-color: white;
        padding: 15px 20px;
        font-weight: 600;
        color: var(--primary-color);
    }

    .stExpander:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }

    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: var(--dark-text);
    }

    h1 {
        font-size: 36px;
        font-weight: 800;
        margin-bottom: 10px;
    }

    h2 {
        font-size: 28px;
        font-weight: 700;
        margin-top: 20px;
        margin-bottom: 15px;
        color: var(--primary-color);
    }

    h3 {
        font-size: 22px;
        font-weight: 600;
        margin-top: 15px;
        margin-bottom: 10px;
        color: var(--secondary-color);
    }

    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        font-weight: 600;
        transition: var(--transition);
        box-shadow: var(--shadow);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }

    .stButton > button[kind="secondary"] {
        background-color: white;
        color: var(--primary-color);
        border: 1px solid var(--primary-color);
    }

    .stButton > button[kind="secondary"]:hover {
        background-color: var(--primary-color);
        color: white;
    }

    /* File uploader */
    .stFileUploader > section {
        border-radius: 10px;
        border: 2px dashed var(--border-color);
        background-color: white;
        padding: 20px;
        transition: var(--transition);
    }

    .stFileUploader > section:hover {
        border-color: var(--primary-color);
        background-color: #f0f5ff;
    }

    /* Success and warning messages */
    .stAlert {
        border-radius: 10px;
        border: none;
        padding: 15px 20px;
        margin-bottom: 15px;
    }

    /* Language toggle styles */
    .language-toggle {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 999;
        display: flex;
        gap: 10px;
    }

    .language-toggle button {
        background-color: white;
        border: 1px solid var(--border-color);
        border-radius: 20px;
        padding: 8px 15px;
        font-weight: 600;
        color: var(--dark-text);
        transition: var(--transition);
        box-shadow: var(--shadow);
    }

    .language-toggle button:hover {
        background-color: var(--primary-color);
        color: white;
        border-color: var(--primary-color);
    }

    /* Data frames */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: var(--shadow);
    }

    /* Footer */
    footer {
        text-align: center;
        padding: 20px;
        color: #6c757d;
        font-size: 14px;
        border-top: 1px solid var(--border-color);
        margin-top: 30px;
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        .function-btn {
            padding: 12px 15px;
            font-size: 14px;
        }

        .function-card {
            padding: 20px;
        }

        h1 {
            font-size: 28px;
        }

        h2 {
            font-size: 24px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Language toggle in top right corner
st.markdown('<div class="language-toggle">', unsafe_allow_html=True)
# Initialize language in session state
if 'language' not in st.session_state:
    st.session_state.language = 'zh'  # Default to Chinese
# Create language toggle buttons
# col1, col2 = st.columns(2)
# with col1:
#     if st.button('English' if st.session_state.language == 'zh' else '🇺🇸 English'):
#         st.session_state.language = 'en'
#         st.rerun()
# with col2:
#     if st.button('中文' if st.session_state.language == 'en' else '🇨🇳 中文'):
#         st.session_state.language = 'zh'
#         st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# Main title
st.title(_("app_title"))

# Determine which function is selected
if 'selected_function' not in st.session_state:
    st.session_state.selected_function = "data_concat"


# Function to create styled buttons
def styled_button(label, function_key, use_container_width=True):
    # Determine button class based on whether it's selected
    button_class = "function-btn selected" if st.session_state.selected_function == function_key else "function-btn"

    # Create the button
    if st.button(label, key=f"{function_key}_btn", use_container_width=use_container_width):
        st.session_state.selected_function = function_key
        st.rerun()

    # Inject CSS to style the button appropriately
    st.markdown(f"""
        <style>
            [key="{function_key}_btn"] {{
                background: {'linear-gradient(90deg, #4361ee 0%, #3f37c9 100%)' if st.session_state.selected_function == function_key else 'white'};
                color: {'white' if st.session_state.selected_function == function_key else '#212529'};
                font-weight: {'600' if st.session_state.selected_function == function_key else '500'};
                box-shadow: {'0 6px 12px rgba(67, 97, 238, 0.3)' if st.session_state.selected_function == function_key else '0 4px 6px rgba(0, 0, 0, 0.1)'};
            }}
            [key="{function_key}_btn"]:hover {{
                background: {'linear-gradient(90deg, #4361ee 0%, #3f37c9 100%)' if st.session_state.selected_function == function_key else '#4361ee'};
                color: {'white' if st.session_state.selected_function == function_key else 'white'};
                transform: {'translateY(-2px)' if st.session_state.selected_function != function_key else 'none'};
                box-shadow: {'0 6px 12px rgba(67, 97, 238, 0.3)' if st.session_state.selected_function == function_key else '0 6px 12px rgba(67, 97, 238, 0.2)'};
            }}
        </style>
    """, unsafe_allow_html=True)


# Sidebar with functional areas
with st.sidebar:

    # Data Transformation Functions
    st.markdown(f'<div class="sidebar-header">{_("data_transformation")}</div>', unsafe_allow_html=True)

    # Create buttons with conditional styling based on selection
    styled_button(_("data_concat"), "data_concat")
    styled_button(_("data_join"), "data_join")
    styled_button(_("sheet_merge"), "sheet_merge")
    styled_button(_("sheet_split"), "sheet_split")

    # Format Conversion Functions
    st.markdown(f'<div class="sidebar-header">{_("format_conversion")}</div>', unsafe_allow_html=True)

    styled_button(_("excel_to_csv"), "excel_to_csv")
    styled_button(_("csv_to_excel"), "csv_to_excel")
    styled_button(_("excel_to_pdf"), "excel_to_pdf")
    styled_button(_("pdf_to_excel"), "pdf_to_excel")

# Main content area
st.markdown(f'<div class="main-header">{_("main_header")}</div>', unsafe_allow_html=True)

# Display the selected function
with st.container():
    st.markdown('<div class="function-card">', unsafe_allow_html=True)

    # Data Concatenation Function
    if st.session_state.selected_function == "data_concat":
        st.header(_("data_concat_header"))

        # Info section with collapsible description
        with st.expander("ℹ️ " + _("功能描述 - 点击查看详情")):
            st.write(_("data_concat_desc"))

        # Initialize session state for this function
        if 'concat_reset_trigger' not in st.session_state:
            st.session_state.concat_reset_trigger = 0

        # File uploader for concatenation with reset capability
        concat_files = st.file_uploader(
            _("select_files_concat"),
            type=["xlsx"],
            accept_multiple_files=True,
            key=f"concat_uploader_{st.session_state.concat_reset_trigger}"
        )

        if concat_files:
            st.subheader(_("file_info"))
            st.write(f"{len(concat_files)} {_('files_selected')}")

            # Display file names and sheet counts
            file_info = []
            dataframes = []
            column_structures = []

            try:
                for file in concat_files:
                    with st.expander(file.name):
                        # Read Excel file
                        excel_file = pd.ExcelFile(file)
                        st.write(f"{_('sheet_count')}: {len(excel_file.sheet_names)}")
                        st.write(f"{_('sheet_list')}: {excel_file.sheet_names}")

                        # Read all sheets and collect data
                        for sheet_name in excel_file.sheet_names:
                            df = pd.read_excel(file, sheet_name=sheet_name)
                            dataframes.append(df)

                            # Record column structure for consistency check
                            columns_info = {
                                'file': file.name,
                                'sheet': sheet_name,
                                'columns': list(df.columns),
                                'dtypes': dict(df.dtypes)
                            }
                            column_structures.append(columns_info)

                # Check structural consistency
                st.subheader(_("structure_check"))
                if len(column_structures) > 0:
                    first_columns = column_structures[0]['columns']
                    first_dtypes = column_structures[0]['dtypes']

                    consistent = True
                    inconsistent_sheets = []

                    for struct in column_structures:
                        if struct['columns'] != first_columns:
                            consistent = False
                            inconsistent_sheets.append(f"{struct['file']} - {struct['sheet']}")

                    if consistent:
                        st.success(_("structure_consistent"))
                    else:
                        st.warning(_("structure_inconsistent"))
                        for sheet in inconsistent_sheets:
                            st.write(f"- {sheet}")
                        st.info(_("only_consistent"))

                # Output file name
                output_filename = st.text_input(_("output_filename"), "concatenated_data.xlsx")

                # Concatenate button
                col1_btn, col2_btn = st.columns(2)
                with col1_btn:
                    if st.button(_("execute_concat")) and len(dataframes) > 0:
                        with st.spinner(_("processing_concat")):
                            try:
                                # Filter dataframes with consistent structure
                                if consistent:
                                    concatenated_df = pd.concat(dataframes, ignore_index=True)

                                    # Convert to Excel
                                    output = BytesIO()
                                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                                        concatenated_df.to_excel(writer, index=False, sheet_name='Concatenated_Data')
                                    output.seek(0)

                                    # Download button
                                    st.download_button(
                                        label=_("download_result"),
                                        data=output,
                                        file_name=output_filename,
                                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                    )

                                    # Preview
                                    st.subheader(_("preview_result"))
                                    st.dataframe(concatenated_df.head())
                                    st.success(_("success_concat").format(len(dataframes)))
                                else:
                                    # Only concatenate consistent dataframes
                                    consistent_dfs = []
                                    for i, df in enumerate(dataframes):
                                        if list(df.columns) == first_columns:
                                            consistent_dfs.append(df)

                                    if len(consistent_dfs) > 0:
                                        concatenated_df = pd.concat(consistent_dfs, ignore_index=True)

                                        # Convert to Excel
                                        output = BytesIO()
                                        with pd.ExcelWriter(output, engine='openpyxl') as writer:
                                            concatenated_df.to_excel(writer, index=False,
                                                                     sheet_name='Concatenated_Data')
                                        output.seek(0)

                                        # Download button
                                        st.download_button(
                                            label=_("download_result"),
                                            data=output,
                                            file_name=output_filename,
                                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                        )

                                        # Preview
                                        st.subheader(_("preview_result"))
                                        st.dataframe(concatenated_df.head())
                                        st.success(_("success_concat_consistent").format(len(consistent_dfs)))
                                    else:
                                        st.error(_("no_consistent_tables"))
                            except Exception as e:
                                st.error(_("error_processing").format(str(e)))

                # Reset button
                with col2_btn:
                    if st.button(_("reset_operation")):
                        st.session_state.concat_reset_trigger += 1
                        st.rerun()

            except Exception as e:
                st.error(_("error_processing").format(str(e)))

    # Data Joining Function
    elif st.session_state.selected_function == "data_join":
        st.header(_("data_join_header"))

        # Info section with collapsible description
        with st.expander("ℹ️ " + _("功能描述 - 点击查看详情")):
            st.write(_("data_join_desc"))

        # Initialize session state for this function
        if 'join_reset_trigger' not in st.session_state:
            st.session_state.join_reset_trigger = 0

        # File uploader for joining with reset capability
        join_files = st.file_uploader(
            _("select_files_join"),
            type=["xlsx"],
            accept_multiple_files=True,
            key=f"join_uploader_{st.session_state.join_reset_trigger}"
        )

        if join_files:
            st.subheader(_("file_info"))
            st.write(f"{len(join_files)} {_('files_selected')}")

            try:
                # Collect all dataframes and their columns
                all_dataframes = []
                all_columns = set()

                for file in join_files:
                    with st.expander(file.name):
                        excel_file = pd.ExcelFile(file)
                        st.write(f"{_('sheet_count')}: {len(excel_file.sheet_names)}")

                        for sheet_name in excel_file.sheet_names:
                            df = pd.read_excel(file, sheet_name=sheet_name)
                            all_dataframes.append(df)
                            all_columns.update(df.columns)
                            st.write(f"Sheet '{sheet_name}' {_('sheet_list')}: {list(df.columns)}")

                # Key field selection
                if len(all_columns) > 0:
                    st.subheader(_("key_field_selection"))
                    key_column = st.selectbox(_("select_key_field"), sorted(list(all_columns)))

                    # Join type selection
                    join_type = st.selectbox(
                        _("select_join_method"),
                        ["left", "inner", "outer"],
                        format_func=lambda x: {
                            "left": _("left_join"),
                            "inner": _("inner_join"),
                            "outer": _("outer_join")
                        }[x]
                    )

                    # Execute join
                    col1_btn, col2_btn = st.columns(2)
                    with col1_btn:
                        if st.button(_("execute_join")):
                            with st.spinner(_("processing_join")):
                                if len(all_dataframes) > 0:
                                    # Check if key column exists in all dataframes
                                    missing_key = []
                                    for i, df in enumerate(all_dataframes):
                                        if key_column not in df.columns:
                                            missing_key.append(i)

                                    if len(missing_key) > 0:
                                        st.warning(_("key_missing").format(key_column))
                                        # Filter dataframes that contain the key column
                                        filtered_dfs = [df for df in all_dataframes if key_column in df.columns]
                                    else:
                                        filtered_dfs = all_dataframes

                                    if len(filtered_dfs) > 0:
                                        # Perform joins
                                        result_df = filtered_dfs[0]
                                        for i in range(1, len(filtered_dfs)):
                                            result_df = pd.merge(result_df, filtered_dfs[i], on=key_column,
                                                                 how=join_type, suffixes=('', f'_df{i + 1}'))

                                        # Convert to Excel
                                        output = BytesIO()
                                        with pd.ExcelWriter(output, engine='openpyxl') as writer:
                                            result_df.to_excel(writer, index=False, sheet_name='Joined_Data')
                                        output.seek(0)

                                        # Download button
                                        st.download_button(
                                            label=_("download_result"),
                                            data=output,
                                            file_name="joined_data.xlsx",
                                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                        )

                                        # Preview and summary
                                        st.subheader(_("preview_result"))
                                        st.dataframe(result_df.head())
                                        st.info(_("join_success_records").format(len(result_df)))
                                        st.success(_("join_success"))
                                    else:
                                        st.error(_("no_valid_tables"))
                                else:
                                    st.error(_("no_valid_tables_found"))

                    # Reset button
                    with col2_btn:
                        if st.button(_("reset_operation")):
                            st.session_state.join_reset_trigger += 1
                            st.rerun()

            except Exception as e:
                st.error(_("error_processing").format(str(e)))

    # Sheet Merging Function
    elif st.session_state.selected_function == "sheet_merge":
        st.header(_("sheet_merge_header"))

        # Info section with collapsible description
        with st.expander("ℹ️ " + _("功能描述 - 点击查看详情")):
            st.write(_("sheet_merge_desc"))

        # Initialize session state for this function
        if 'merge_reset_trigger' not in st.session_state:
            st.session_state.merge_reset_trigger = 0

        # File uploader for merging with reset capability
        merge_files = st.file_uploader(
            _("select_files_merge"),
            type=["xlsx"],
            accept_multiple_files=True,
            key=f"merge_uploader_{st.session_state.merge_reset_trigger}"
        )

        if merge_files:
            st.subheader(_("file_info"))
            st.write(f"{len(merge_files)} {_('files_selected')}")

            try:
                col1_btn, col2_btn = st.columns(2)
                with col1_btn:
                    if st.button(_("execute_merge")):
                        with st.spinner(_("processing_merge")):
                            # Create a new workbook for merged sheets
                            merged_wb = Workbook()
                            # Remove the default sheet
                            merged_wb.remove(merged_wb.active)

                            sheet_count = 0
                            file_count = len(merge_files)

                            # Process each file
                            for file in merge_files:
                                # Load the workbook
                                xl_file = pd.ExcelFile(file)

                                # Process each sheet in the file
                                for sheet_name in xl_file.sheet_names:
                                    # Read the sheet
                                    df = pd.read_excel(file, sheet_name=sheet_name)

                                    # Create a unique sheet name if needed
                                    unique_sheet_name = sheet_name
                                    counter = 1
                                    while unique_sheet_name in [ws.title for ws in merged_wb.worksheets]:
                                        unique_sheet_name = f"{sheet_name}_{counter}"
                                        counter += 1

                                    # Create new worksheet
                                    ws = merged_wb.create_sheet(title=unique_sheet_name)

                                    # Write data to worksheet
                                    for r in dataframe_to_rows(df, index=False, header=True):
                                        ws.append(r)

                                    sheet_count += 1

                            # Save to BytesIO
                            output = BytesIO()
                            merged_wb.save(output)
                            output.seek(0)

                            # Download button
                            st.download_button(
                                label=_("download_result"),
                                data=output,
                                file_name="merged_sheets.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            )

                            # Summary
                            st.success(_("success_merge").format(file_count, sheet_count))

                # Reset button
                with col2_btn:
                    if st.button(_("reset_operation")):
                        st.session_state.merge_reset_trigger += 1
                        st.rerun()

            except Exception as e:
                st.error(_("error_processing").format(str(e)))

    # Sheet Splitting Function
    elif st.session_state.selected_function == "sheet_split":
        st.header(_("sheet_split_header"))

        # Info section with collapsible description
        with st.expander("ℹ️ " + _("功能描述 - 点击查看详情")):
            st.write(_("sheet_split_desc"))

        # Initialize session state for this function
        if 'split_reset_trigger' not in st.session_state:
            st.session_state.split_reset_trigger = 0

        # File uploader for splitting with reset capability
        split_file = st.file_uploader(
            _("select_file_split"),
            type=["xlsx"],
            accept_multiple_files=False,
            key=f"split_uploader_{st.session_state.split_reset_trigger}"
        )

        if split_file:
            try:
                # Get file name without extension
                base_name = os.path.splitext(split_file.name)[0]

                # Read Excel file
                excel_file = pd.ExcelFile(split_file)
                sheet_names = excel_file.sheet_names

                st.subheader(_("file_info"))
                st.write(f"{_('file_name')}: {split_file.name}")
                st.write(f"{_('sheet_count')}: {len(sheet_names)}")
                st.write(f"{_('sheet_list')}: {sheet_names}")

                # Execute split
                col1_btn, col2_btn = st.columns(2)
                with col1_btn:
                    if st.button(_("execute_split")):
                        with st.spinner(_("processing_split")):
                            # Create in-memory zip file
                            zip_buffer = BytesIO()

                            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                                # Process each sheet
                                for sheet_name in sheet_names:
                                    # Read the sheet
                                    df = pd.read_excel(split_file, sheet_name=sheet_name)

                                    # Create filename for this sheet
                                    sheet_filename = f"{base_name}_{sheet_name}.xlsx"

                                    # Convert to Excel in memory
                                    sheet_buffer = BytesIO()
                                    with pd.ExcelWriter(sheet_buffer, engine='openpyxl') as writer:
                                        df.to_excel(writer, index=False, sheet_name=sheet_name)
                                    sheet_buffer.seek(0)

                                    # Add to zip
                                    zip_file.writestr(sheet_filename, sheet_buffer.getvalue())

                            # Prepare zip for download
                            zip_buffer.seek(0)

                            # Download button
                            st.download_button(
                                label=_("download_split_result"),
                                data=zip_buffer,
                                file_name=f"{base_name}_sheets.zip",
                                mime="application/zip"
                            )

                            # Summary
                            st.success(_("success_split").format(len(sheet_names)))
                            st.write(_("split_sheets"))
                            for name in sheet_names:
                                st.write(f"- {base_name}_{name}.xlsx")

                # Reset button
                with col2_btn:
                    if st.button(_("reset_operation")):
                        st.session_state.split_reset_trigger += 1
                        st.rerun()

            except Exception as e:
                st.error(_("error_processing").format(str(e)))

    # Excel to CSV Converter
    elif st.session_state.selected_function == "excel_to_csv":
        st.header(_("excel_to_csv_header"))

        # Info section with collapsible description
        with st.expander("ℹ️ " + _("功能描述 - 点击查看详情")):
            st.write(_("excel_to_csv_desc"))

        # Initialize session state for this function
        if 'excel_to_csv_reset_trigger' not in st.session_state:
            st.session_state.excel_to_csv_reset_trigger = 0

        # File uploader for Excel files with reset capability
        excel_files = st.file_uploader(
            _("select_excel_files"),
            type=["xlsx"],
            accept_multiple_files=True,
            key=f"excel_to_csv_uploader_{st.session_state.excel_to_csv_reset_trigger}"
        )

        if excel_files:
            try:
                st.subheader(_("file_info"))
                st.write(f"{len(excel_files)} {_('files_selected')}")

                # Show file details
                for file in excel_files:
                    with st.expander(file.name):
                        excel_file = pd.ExcelFile(file)
                        st.write(f"{_('sheet_count')}: {len(excel_file.sheet_names)}")
                        st.write(f"{_('sheet_list')}: {excel_file.sheet_names}")

                # Convert button
                col1_btn, col2_btn = st.columns(2)
                with col1_btn:
                    if st.button(_("execute_conversion")):
                        with st.spinner(_("processing_excel_csv")):
                            # Create in-memory zip file
                            zip_buffer = BytesIO()

                            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                                # Process each Excel file
                                for file in excel_files:
                                    # Get base name without extension
                                    base_name = os.path.splitext(file.name)[0]

                                    # Read Excel file
                                    excel_file = pd.ExcelFile(file)

                                    # Process each sheet
                                    for sheet_name in excel_file.sheet_names:
                                        # Read the sheet
                                        df = pd.read_excel(file, sheet_name=sheet_name)

                                        # Convert to CSV in memory with proper encoding for Chinese characters
                                        csv_buffer = BytesIO()
                                        df.to_csv(csv_buffer, index=False, encoding='utf-8-sig')
                                        csv_buffer.seek(0)

                                        # Create filename for this CSV
                                        if len(excel_files) == 1:
                                            csv_filename = f"{base_name}_{sheet_name}.csv"
                                        else:
                                            csv_filename = f"{base_name}_{sheet_name}.csv"

                                        # Add to zip
                                        zip_file.writestr(csv_filename, csv_buffer.getvalue())

                            # Prepare zip for download
                            zip_buffer.seek(0)

                            # Download button
                            st.download_button(
                                label=_("download_csv_zip"),
                                data=zip_buffer,
                                file_name="excel_to_csv_converted.zip",
                                mime="application/zip"
                            )

                            # Summary
                            st.success(_("success_excel_csv").format(len(excel_files)))

                # Reset button
                with col2_btn:
                    if st.button(_("reset_operation")):
                        st.session_state.excel_to_csv_reset_trigger += 1
                        st.rerun()

            except Exception as e:
                st.error(_("error_processing").format(str(e)))

    # CSV to Excel Converter
    elif st.session_state.selected_function == "csv_to_excel":
        st.header(_("csv_to_excel_header"))

        # Info section with collapsible description
        with st.expander("ℹ️ " + _("功能描述 - 点击查看详情")):
            st.write(_("csv_to_excel_desc"))

        # Initialize session state for this function
        if 'csv_to_excel_reset_trigger' not in st.session_state:
            st.session_state.csv_to_excel_reset_trigger = 0

        # File uploader for CSV files with reset capability
        csv_files = st.file_uploader(
            _("select_csv_files"),
            type=["csv"],
            accept_multiple_files=True,
            key=f"csv_to_excel_uploader_{st.session_state.csv_to_excel_reset_trigger}"
        )

        if csv_files:
            try:
                st.subheader(_("file_info"))
                st.write(f"{len(csv_files)} {_('files_selected')}")

                # Show file names
                for file in csv_files:
                    st.write(f"- {file.name}")

                # Convert button
                col1_btn, col2_btn = st.columns(2)
                with col1_btn:
                    if st.button(_("execute_conversion")):
                        with st.spinner(_("processing_csv_excel")):
                            # Create in-memory zip file
                            zip_buffer = BytesIO()

                            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                                # Process each CSV file
                                for file in csv_files:
                                    # Get base name without extension
                                    base_name = os.path.splitext(file.name)[0]

                                    # Read the CSV with encoding detection
                                    try:
                                        # First try UTF-8
                                        df = pd.read_csv(file)
                                    except UnicodeDecodeError:
                                        # If UTF-8 fails, try other common encodings
                                        try:
                                            # Reset file pointer to beginning
                                            file.seek(0)
                                            # Try GBK (common for Chinese CSV files)
                                            df = pd.read_csv(file, encoding='gbk')
                                        except UnicodeDecodeError:
                                            try:
                                                # Reset file pointer to beginning
                                                file.seek(0)
                                                # Try Latin-1 (covers all 256 possible byte values)
                                                df = pd.read_csv(file, encoding='latin-1')
                                            except UnicodeDecodeError:
                                                # Reset file pointer to beginning
                                                file.seek(0)
                                                # As a last resort, use UTF-8 with error handling
                                                df = pd.read_csv(file, encoding='utf-8', encoding_errors='ignore')

                                    # Convert to Excel in memory
                                    excel_buffer = BytesIO()
                                    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                                        df.to_excel(writer, index=False, sheet_name='Sheet1')
                                    excel_buffer.seek(0)

                                    # Create filename for this Excel file
                                    excel_filename = f"{base_name}.xlsx"

                                    # Add to zip
                                    zip_file.writestr(excel_filename, excel_buffer.getvalue())

                            # Prepare zip for download
                            zip_buffer.seek(0)

                            # Download button
                            st.download_button(
                                label=_("download_excel_zip"),
                                data=zip_buffer,
                                file_name="csv_to_excel_converted.zip",
                                mime="application/zip"
                            )

                            # Summary
                            st.success(_("success_csv_excel").format(len(csv_files)))

                # Reset button
                with col2_btn:
                    if st.button(_("reset_operation")):
                        st.session_state.csv_to_excel_reset_trigger += 1
                        st.rerun()

            except Exception as e:
                st.error(_("error_processing").format(str(e)))

    # Excel to PDF Converter
    elif st.session_state.selected_function == "excel_to_pdf":
        st.header(_("excel_to_pdf_header"))

        # Info section with collapsible description
        with st.expander("ℹ️ " + _("功能描述 - 点击查看详情")):
            st.write(_("excel_to_pdf_desc"))

        # Initialize session state for this function
        if 'excel_to_pdf_reset_trigger' not in st.session_state:
            st.session_state.excel_to_pdf_reset_trigger = 0

        # File uploader for Excel files with reset capability
        excel_files = st.file_uploader(
            _("select_excel_files"),
            type=["xlsx"],
            accept_multiple_files=True,
            key=f"excel_to_pdf_uploader_{st.session_state.excel_to_pdf_reset_trigger}"
        )

        if excel_files:
            try:
                st.subheader(_("file_info"))
                st.write(f"{len(excel_files)} {_('files_selected')}")

                # Show file details
                for file in excel_files:
                    with st.expander(file.name):
                        excel_file = pd.ExcelFile(file)
                        st.write(f"{_('sheet_count')}: {len(excel_file.sheet_names)}")
                        st.write(f"{_('sheet_list')}: {excel_file.sheet_names}")

                # Convert button
                col1_btn, col2_btn = st.columns(2)
                with col1_btn:
                    if st.button(_("execute_conversion")):
                        with st.spinner(_("processing_excel_pdf")):
                            # Try to find a font that supports Chinese characters
                            # Common Chinese fonts
                            chinese_fonts = ['SimHei', 'Microsoft YaHei', 'STHeiti', 'SimSun', 'FangSong']
                            font_prop = None

                            # Try to find a suitable font
                            for font_name in chinese_fonts:
                                try:
                                    font_prop = fm.FontProperties(
                                        fname=fm.findfont(fm.FontProperties(family=font_name)))
                                    break
                                except:
                                    continue

                            # If no Chinese font found, use default font but with utf-8 support
                            if font_prop is None:
                                font_prop = fm.FontProperties()

                            # Create in-memory zip file
                            zip_buffer = BytesIO()

                            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                                # Process each Excel file
                                for file in excel_files:
                                    # Get base name without extension
                                    base_name = os.path.splitext(file.name)[0]

                                    # Read Excel file
                                    excel_file = pd.ExcelFile(file)

                                    # Process each sheet
                                    for sheet_name in excel_file.sheet_names:
                                        # Read the sheet
                                        df = pd.read_excel(file, sheet_name=sheet_name)

                                        # Convert DataFrame to PDF using matplotlib
                                        fig, ax = plt.subplots(figsize=(12, 8))
                                        ax.axis('tight')
                                        ax.axis('off')

                                        # Create table
                                        table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center',
                                                         loc='center')
                                        table.auto_set_font_size(False)
                                        table.set_fontsize(8)
                                        table.scale(1.2, 1.2)

                                        # Set font properties for table
                                        for key, cell in table.get_celld().items():
                                            cell.set_text_props(fontproperties=font_prop)

                                        # Set title with proper font
                                        plt.title(f"{sheet_name}", fontsize=16, pad=20, fontproperties=font_prop)

                                        # Save to PDF in memory
                                        pdf_buffer = BytesIO()
                                        plt.savefig(pdf_buffer, format='pdf', bbox_inches='tight', dpi=300)
                                        pdf_buffer.seek(0)
                                        plt.close(fig)

                                        # Create filename for this PDF
                                        pdf_filename = f"{base_name}_{sheet_name}.pdf"

                                        # Add to zip
                                        zip_file.writestr(pdf_filename, pdf_buffer.getvalue())

                            # Prepare zip for download
                            zip_buffer.seek(0)

                            # Download button
                            st.download_button(
                                label=_("download_pdf_zip"),
                                data=zip_buffer,
                                file_name="excel_to_pdf_converted.zip",
                                mime="application/zip"
                            )

                            # Summary
                            st.success(_("success_excel_pdf").format(len(excel_files)))

                # Reset button
                with col2_btn:
                    if st.button(_("reset_operation")):
                        st.session_state.excel_to_pdf_reset_trigger += 1
                        st.rerun()

            except Exception as e:
                st.error(_("error_processing").format(str(e)))

    # PDF to Excel Converter
    elif st.session_state.selected_function == "pdf_to_excel":
        st.header(_("pdf_to_excel_header"))

        # Info section with collapsible description
        with st.expander("ℹ️ " + _("功能描述 - 点击查看详情")):
            st.write(_("pdf_to_excel_desc"))

        # Initialize session state for this function
        if 'pdf_to_excel_reset_trigger' not in st.session_state:
            st.session_state.pdf_to_excel_reset_trigger = 0

        # File uploader for PDF files with reset capability
        pdf_files = st.file_uploader(
            _("select_pdf_files"),
            type=["pdf"],
            accept_multiple_files=True,
            key=f"pdf_to_excel_uploader_{st.session_state.pdf_to_excel_reset_trigger}"
        )

        if pdf_files:
            try:
                st.subheader(_("file_info"))
                st.write(f"{len(pdf_files)} {_('files_selected')}")

                # Show file names
                for file in pdf_files:
                    st.write(f"- {file.name}")

                # Convert button
                col1_btn, col2_btn = st.columns(2)
                with col1_btn:
                    if st.button(_("execute_conversion"),
                                 key=f"pdf_convert_btn_{st.session_state.pdf_to_excel_reset_trigger}"):
                        with st.spinner(_("processing_pdf_excel")):
                            # Create in-memory zip file
                            zip_buffer = BytesIO()

                            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                                # Process each PDF file
                                for idx, file in enumerate(pdf_files):
                                    # Get base name without extension
                                    base_name = os.path.splitext(file.name)[0]

                                    # Save file to temporary location to avoid stream issues
                                    temp_file_path = os.path.join(os.getcwd(), f"temp_{base_name}_{idx}.pdf")
                                    with open(temp_file_path, "wb") as temp_file:
                                        temp_file.write(file.getvalue())

                                    try:
                                        # Extract tables from PDF using pdfplumber
                                        with pdfplumber.open(temp_file_path) as pdf:
                                            all_tables = []

                                            # Process each page
                                            for page_num, page in enumerate(pdf.pages):
                                                # Extract tables from the page
                                                tables = page.extract_tables()

                                                # Process each table
                                                for table_num, table in enumerate(tables):
                                                    if table:  # Check if table is not empty
                                                        # Convert table to DataFrame
                                                        df = pd.DataFrame(table[1:],
                                                                          columns=table[0])  # First row as headers
                                                        all_tables.append(df)

                                            # If tables were found, convert them to Excel
                                            if all_tables:
                                                # Convert to Excel in memory
                                                excel_buffer = BytesIO()
                                                with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                                                    # Write each table to a separate sheet
                                                    for i, df in enumerate(all_tables):
                                                        sheet_name = f"Table_{i + 1}"
                                                        # Limit sheet name to 31 characters (Excel limit)
                                                        if len(sheet_name) > 31:
                                                            sheet_name = sheet_name[:31]
                                                        df.to_excel(writer, index=False, sheet_name=sheet_name)
                                                excel_buffer.seek(0)

                                                # Create filename for this Excel file
                                                excel_filename = f"{base_name}_extracted_tables.xlsx"

                                                # Add to zip
                                                zip_file.writestr(excel_filename, excel_buffer.getvalue())
                                            else:
                                                # No tables found, create a placeholder
                                                placeholder_df = pd.DataFrame(
                                                    [{"Message": "No tables found in this PDF"}])
                                                excel_buffer = BytesIO()
                                                with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                                                    placeholder_df.to_excel(writer, index=False,
                                                                            sheet_name='No_Tables_Found')
                                                excel_buffer.seek(0)

                                                # Create filename for this Excel file
                                                excel_filename = f"{base_name}_no_tables_found.xlsx"

                                                # Add to zip
                                                zip_file.writestr(excel_filename, excel_buffer.getvalue())

                                    except Exception as pdf_error:
                                        st.warning(
                                            f"Processing file {file.name} encountered an issue: {str(pdf_error)}")
                                        # Create error report
                                        error_df = pd.DataFrame(
                                            [{"Error": f"Failed to process {file.name}", "Details": str(pdf_error)}])
                                        excel_buffer = BytesIO()
                                        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                                            error_df.to_excel(writer, index=False, sheet_name='Error_Report')
                                        excel_buffer.seek(0)

                                        # Create filename for this Excel file
                                        excel_filename = f"{base_name}_error_report.xlsx"

                                        # Add to zip
                                        zip_file.writestr(excel_filename, excel_buffer.getvalue())
                                    finally:
                                        # Clean up temporary file
                                        if os.path.exists(temp_file_path):
                                            os.remove(temp_file_path)

                            # Prepare zip for download
                            zip_buffer.seek(0)

                            # Store the result in session state to avoid recreating elements
                            st.session_state.pdf_to_excel_result = zip_buffer
                            st.session_state.pdf_to_excel_processed = True

                # Show download button and success message if processing is done
                if 'pdf_to_excel_processed' in st.session_state and st.session_state.pdf_to_excel_processed:
                    # Download button
                    st.download_button(
                        label=_("download_excel_zip"),
                        data=st.session_state.pdf_to_excel_result,
                        file_name="pdf_to_excel_converted.zip",
                        mime="application/zip",
                        key=f"pdf_download_btn_{st.session_state.pdf_to_excel_reset_trigger}"
                    )

                    # Summary
                    st.success(_("success_pdf_excel").format(len(pdf_files)))

                # Reset button
                with col2_btn:
                    if st.button(_("reset_operation"),
                                 key=f"pdf_reset_btn_{st.session_state.pdf_to_excel_reset_trigger}"):
                        st.session_state.pdf_to_excel_reset_trigger += 1
                        if 'pdf_to_excel_processed' in st.session_state:
                            del st.session_state.pdf_to_excel_processed
                        if 'pdf_to_excel_result' in st.session_state:
                            del st.session_state.pdf_to_excel_result
                        st.rerun()

            except Exception as e:
                st.error(_("error_processing").format(str(e)))

    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption(_("footer"))