import {NavLink} from 'react-router-dom';
import './Header.scss';

export const Header = () => {
    return (
        <header className="app-header">
            <nav>
                <ul className="nav-list">
                    <li>
                        <NavLink
                            to="/"
                            className={({isActive}) => isActive ? 'active' : ''}
                        >
                            Главная
                        </NavLink>
                    </li>
                    <li>
                        <NavLink
                            to="/parameters"
                            className={({isActive}) => isActive ? 'active' : ''}
                        >
                            Задать параметры
                        </NavLink>
                    </li>
                    <li>
                        <NavLink
                            to="/calculator"
                            className={({isActive}) => isActive ? 'active' : ''}
                        >
                            Калькулятор
                        </NavLink>
                    </li>
                    <li>
                        <NavLink
                            to="/probabilities"
                            className={({isActive}) => isActive ? 'active' : ''}
                        >
                            Посчитать вероятности
                        </NavLink>
                    </li>
                </ul>
            </nav>
        </header>
    );
};