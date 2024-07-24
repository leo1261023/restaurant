import React from 'react';
import { Link } from 'react-router-dom';
import '../App.css'; // 確保路徑正確

function UpTitle() {
  return (
    <div className="UpTitle">
      <div className="navbar">
        <h1 className="title">台北餐廳推薦系統</h1>
        <div className="nav-links">
          <Link to="/member">會員</Link>
          <a href="#">登出</a>
        </div>
      </div>
    </div>
  );
}

export default UpTitle;
