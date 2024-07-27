import React, { useEffect, useState } from 'react';
import { useLocation, Link } from 'react-router-dom';
import '../App.css';

function Rec() {
    const [filteredRestaurants, setFilteredRestaurants] = useState([]);
    const location = useLocation();

    useEffect(() => {
        const params = new URLSearchParams(location.search);
        const area = params.get('area');
        const cuisine = params.get('cuisine');

        fetch('/restaurants_data.json')
            .then(response => response.json())
            .then(data => {
                let filteredByArea = data;
                let filteredByCuisine = data;

                // 如果有區域條件，先過濾符合區域的餐廳
                if (area) {
                    filteredByArea = data.filter(restaurant => restaurant.query === area);
                }

                // 如果有菜系條件，過濾符合菜系的餐廳
                if (cuisine) {
                    filteredByCuisine = data.filter(restaurant => restaurant.query === cuisine);
                }

                // 如果同時有兩個條件，找出同時出現在兩個篩選結果中的餐廳
                let finalFiltered = filteredByArea.filter(restaurant => 
                    filteredByCuisine.some(cuisineRestaurant => cuisineRestaurant.name === restaurant.name)
                );

                // 使用 Set 來確保每個餐廳只出現一次
                const uniqueRestaurants = Array.from(new Set(finalFiltered.map(r => r.name)))
                    .map(name => {
                        return finalFiltered.find(restaurant => restaurant.name === name);
                    });

                setFilteredRestaurants(uniqueRestaurants);
            })
            .catch(error => console.error('Error fetching data:', error));
    }, [location.search]);

    return (
        <div className="rec-container">
            <div className="rec-content">
                <h1 className="rec-section-title">搜尋結果</h1>
                <Link to="/">
                    <button className="button">回首頁</button>
                </Link>
                <div className="rec-restaurant-list">
                    {filteredRestaurants.length > 0 ? (
                        filteredRestaurants.map((restaurant, index) => (
                            <div key={index} className="rec-restaurant-item">
                                <img src={restaurant.image || 'default-image-url.jpg'} alt={restaurant.name} />
                                <a href={restaurant.href} target="_blank" rel="noopener noreferrer">
                                    {restaurant.name}
                                </a>
                            </div>
                        ))
                    ) : (
                        <p>很抱歉，沒有符合餐廳</p>
                    )}
                </div>
            </div>
        </div>
    );
}

export default Rec;
