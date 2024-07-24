import React from 'react';
import { Link } from 'react-router-dom';
import '../App.css';

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
          <button className="button">註冊</button>
          <Link to="/member">
            <button className="button">返回</button>
          </Link>
        </div>
        <Link to="/">
          <button className="button home-button">回首頁</button>
        </Link>
      </div>
    </div>
  );
}

export default Signin;
