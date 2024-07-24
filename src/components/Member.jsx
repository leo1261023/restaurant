import React from 'react';
import { Link } from 'react-router-dom';
import '../App.css';

function Member() {
  return (
    <div className="member-container">
      <div className="member-content">
        <h1>會員登入</h1>
        <label>帳號</label>
        <input type="text" />
        <label>密碼</label>
        <input type="password" />
        <div className="buttons">
          <Link to="/signin">
            <button className="button">註冊</button>
          </Link>
          <button className="button">登入</button>
        </div>
        <Link to="/">
          <button className="button home-button">回首頁</button>
        </Link>
      </div>
    </div>
  );
}

export default Member;
