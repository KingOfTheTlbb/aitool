import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import NoResultFound
import os
import sys

# 数据库配置
DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/aichat?charset=utf8mb4"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 用户模型
class User(Base):
    __tablename__ = "sys_user"
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, unique=True, index=True)
    password = Column(String)


def home():
    st.markdown(
        """
        <style>
            div[data-testid="stSidebarCollapsedControl"]{
                display: none;
            }
            section[data-testid="stSidebar"][aria-expanded="true"]{
                display: none;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.title("登录")
    username = st.text_input("用户名")
    password = st.text_input("密码", type="password")

    if st.button("登录"):
        session = SessionLocal()
        try:
            user = session.query(User).filter_by(user_name=username).one()
            if user.password == password:
                st.session_state.logged_in = True
                st.session_state.user_id = user.id
                st.session_state.user_name = user.user_name
                # st.rerun()
                command = f"streamlit run 首页.py"  # 根据你的环境调整命令路径和名称
                os.system(command)  # 或者使用 subprocess.run(command, shell=True)
                sys.exit()
            else:
                st.error("当前登录名或密码不正确")
        except NoResultFound:
            st.error("当前登录名或密码不正确")
        finally:
            session.close()

# 主应用逻辑
def run():
    page = st.sidebar.radio("Select a page:", ["Home", "About"])
    if page == "Home":
        home()

if __name__ == "__main__":
    run()