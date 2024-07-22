import React from 'react';
import { Link } from 'react-router-dom';

function UpTitle() {
  return (
    <div className="UpTitle">
      <div className="navbar">
        <div className="title">台北餐廳推薦系統</div>
        <div className="nav-links">
          <Link to="/member">會員</Link>
          <a href="#">登出</a>
        </div>
      </div>
    </div>
  );
}

export default UpTitle;
