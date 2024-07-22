import React from 'react';
import { Link } from 'react-router-dom';
import '../App.css'; // 確保路徑正確


function Rec() {
    return (
      <div className="rec-container">
      <div className="rec-content">
        <h1>餐廳條件</h1>
        <label>
                    菜系
                    <select>
                        <option value="chinese">中式</option>
                        <option value="japanese">日式</option>
                        <option value="italian">美式</option>
                        <option value="mexican"></option>
                    </select>
                </label>
                <label>
                    地區
                    <select>
                        <option value="taipei">台北</option>
                        <option value="taichung">台中</option>
                        <option value="kaohsiung">高雄</option>
                        <option value="tainan">台南</option>
      
                    </select>
                </label>
        <div className="buttons">
          <button>搜尋</button>
        </div>
        <Link to="/">
          <button className="home-button">回首頁</button>
        </Link>
      </div>
    </div>
    );
  }

export default Rec;
