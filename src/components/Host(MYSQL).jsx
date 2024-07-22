import React, { useEffect, useState } from 'react';
import axios from 'axios';
import '../App.css'; // 假設您的 CSS 文件名為 styles.css

function Host() {
    const [restaurants, setRestaurants] = useState([]);

    useEffect(() => {
        axios.get('http://localhost:5000/restaurants')
            .then(response => setRestaurants(response.data))
            .catch(error => console.error('Error fetching data:', error));
    }, []);

    const slideLeft = () => {
        const grid = document.querySelector('.restaurant-grid');
        const itemWidth = document.querySelector('.restaurant-item').offsetWidth + 20; // 餐廳項目的寬度加上間距
        grid.scrollBy({ left: -itemWidth * 5, behavior: 'smooth' });
    };

    const slideRight = () => {
        const grid = document.querySelector('.restaurant-grid');
        const itemWidth = document.querySelector('.restaurant-item').offsetWidth + 20; // 餐廳項目的寬度加上間距
        if (grid.scrollLeft + grid.clientWidth >= grid.scrollWidth) {
            grid.scrollTo({ left: 0, behavior: 'smooth' });
        } else {
            grid.scrollBy({ left: itemWidth * 5, behavior: 'smooth' });
        }
    };

    return (
        <div className="HostRes">
            <div className="search-container">
                <div className="search-content">
                    <h1>餐廳搜尋</h1>
                    <label>
                        菜系
                        <select>
                            <option value="chinese">中式</option>
                            <option value="japanese">日式</option>
                            <option value="italian">美式</option>
                            <option value="mexican">墨西哥菜</option>
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
                </div>
            </div>
            <h1>人氣餐廳</h1>
            <div className="carousel-container">
                <button className="slide-button left" onClick={slideLeft}>&#10094;</button>
                <div className="restaurant-grid">
                    {restaurants.map((restaurant, index) => (
                        <div key={index} className="restaurant-item">
                            <img src={restaurant.rest_image} alt={restaurant.rest_name} />
                            <a href={restaurant.rest_href} target="_blank" rel="noopener noreferrer">
                                {restaurant.rest_name}
                            </a>
                        </div>
                    ))}
                </div>
                <button className="slide-button right" onClick={slideRight}>&#10095;</button>
            </div>
        </div>
    );
}

export default Host;
