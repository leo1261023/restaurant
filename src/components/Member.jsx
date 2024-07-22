import React from 'react';
import { Link } from 'react-router-dom';
import '../App.css'; // 確保路徑正確

function Member() {
  return (
    <div className="member-container">
      <div className="member-content">
        <h1>會員登入</h1>
        <label>帳號<input type="text" /></label>
        <label>密碼<input type="password" /></label>
        <div className="buttons">
        <Link to="/signin">
            <button>註冊</button>
          </Link>
          <button>登入</button>
        </div>
        <Link to="/">
          <button className="home-button">回首頁</button>
        </Link>
      </div>
    </div>
  );
}

export default Member;
