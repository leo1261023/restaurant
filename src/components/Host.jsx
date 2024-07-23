import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../App.css';
import * as XLSX from 'xlsx';

function Host() {
    const [restaurants, setRestaurants] = useState([]);
    const [topRestaurants, setTopRestaurants] = useState([]);
    const [cuisine, setCuisine] = useState('');
    const [area, setArea] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        fetch('/restaurants_data.xlsx')
            .then(response => response.arrayBuffer())
            .then(data => {
                const workbook = XLSX.read(data, { type: 'array' });
                const sheetName = workbook.SheetNames[0];
                const sheet = workbook.Sheets[sheetName];
                const jsonData = XLSX.utils.sheet_to_json(sheet);
                setRestaurants(jsonData);
            })
            .catch(error => console.error('Error fetching data:', error));

        fetch('/toprestaurants.json')
            .then(response => response.json())
            .then(data => setTopRestaurants(data))
            .catch(error => console.error('Error fetching data:', error));
    }, []);

    const handleSearch = () => {
        const params = new URLSearchParams({ cuisine, area });
        navigate(`/rec?${params.toString()}`);
    };

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
                <h1 className="section-title">餐廳搜尋</h1>
                <div className="search-input-container">
                    <select className="search-select" onChange={e => setCuisine(e.target.value)}>
                        <option value="" disabled selected hidden>菜系</option>
                        <option value="中式">中式</option>
                        <option value="日式">日式</option>
                        <option value="美式">美式</option>
                        <option value="墨西哥菜">墨西哥菜</option>
                        <option value="泰式">泰式</option>
                        <option value="韓式">韓式</option>
                        <option value="印度菜">印度菜</option>
                        <option value="法式">法式</option>
                        <option value="越南菜">越南菜</option>
                        <option value="地中海料理">地中海料理</option>
                        <option value="素食">素食</option>
                        <option value="海鮮">海鮮</option>
                    </select>
                    <select className="search-select" onChange={e => setArea(e.target.value)}>
                        <option value="" disabled selected hidden>地區</option>
                        <option value="中正區">中正區</option>
                        <option value="大同區">大同區</option>
                        <option value="中山區">中山區</option>
                        <option value="松山區">松山區</option>
                        <option value="大安區">大安區</option>
                        <option value="萬華區">萬華區</option>                     
                        <option value="信義區">信義區</option>
                        <option value="士林區">士林區</option>
                        <option value="北投區">北投區</option>
                        <option value="內湖區">內湖區</option>
                        <option value="南港區">南港區</option>
                        <option value="文山區">文山區</option>
                    </select>
                    <button className="search-button" onClick={handleSearch}>搜尋</button>
                </div>
            </div>
            <h1 className="section-title">人氣餐廳</h1>
            <div className="carousel-container">
                <button className="slide-button left" onClick={slideLeft}>&#10094;</button>
                <div className="restaurant-grid">
                    {topRestaurants.map((restaurant, index) => (
                        <div key={index} className="restaurant-item">
                            <img src={restaurant.image} alt={restaurant.name} />
                            <a href={restaurant.href} target="_blank" rel="noopener noreferrer">
                                {restaurant.name}
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
