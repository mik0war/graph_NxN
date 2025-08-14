import { Link } from 'react-router-dom';
import '../styles/HomePage.scss';

export const HomePage = () => {
    return (
        <div className="home-page">
            <section className="hero-section">
                <div className="container">
                    <h1>Анализ вероятностей и расчеты</h1>
                    <p className="subtitle">
                        Инструмент для анализа данных, вероятностных расчетов и статистического моделирования
                    </p>
                    <div className="cta-buttons">
                        <Link to="/parameters" className="btn primary">
                            Начать работу
                        </Link>
                        <Link to="/calculator" className="btn secondary">
                            Попробовать калькулятор
                        </Link>
                    </div>
                </div>
            </section>

            <section className="features-section">
                <div className="container">
                    <h2>Основные возможности</h2>
                    <div className="features-grid">
                        <div className="feature-card">
                            <div className="icon">📊</div>
                            <h3>Задание параметров</h3>
                            <p>Гибкая настройка входных параметров для анализа</p>
                        </div>
                        <div className="feature-card">
                            <div className="icon">🧮</div>
                            <h3>Мощный калькулятор</h3>
                            <p>Выполнение сложных вычислений и преобразований</p>
                        </div>
                        <div className="feature-card">
                            <div className="icon">📈</div>
                            <h3>Вероятностный анализ</h3>
                            <p>Расчет и визуализация вероятностных распределений</p>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    );
};