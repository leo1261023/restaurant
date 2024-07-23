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
                // 過濾符合條件的餐廳
                const filtered = data.filter(restaurant => {
                    const matchArea = area ? restaurant.query.includes(area) : true;
                    const matchCuisine = cuisine ? restaurant.query.includes(cuisine) : true;
                    return matchArea && matchCuisine;
                });

                setFilteredRestaurants(filtered);
            })
            .catch(error => console.error('Error fetching data:', error));
    }, [location.search]);

    return (
        <div className="rec-container">
            <div className="rec-content">
                <h1 className="rec-section-title">搜尋結果</h1>
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
                        <p>没有找到符合条件的餐厅。</p>
                    )}
                </div>
                <Link to="/">
                    <button className="rec-home-button">回首頁</button>
                </Link>
            </div>
        </div>
    );
}

export default Rec;
