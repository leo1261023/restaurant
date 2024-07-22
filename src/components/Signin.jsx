import React from 'react';
import { Link } from 'react-router-dom';
import '../App.css'; // 確保路徑正確

function Signin() {
  return (
    <div className="member-container">
      <div className="member-content">
        <h1>會員註冊</h1>
        <label>姓名</label>
        <input type="text" />
        <label>信箱</label>
        <input type="text" />
        <label>帳號</label>
        <input type="text" />
        <label>密碼</label>
        <input type="password" />
        <div className="buttons">
          <button>註冊</button>
          <Link to="/member">
          <button >返回</button>
        </Link>
        </div>
        <Link to="/">
          <button className="home-button">回首頁</button>
        </Link>
      </div>
    </div>
  );
}

export default Signin;
