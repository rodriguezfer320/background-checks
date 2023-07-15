import React from "react";
import { useResolvedPath, useMatch, NavLink, useLocation, matchPath } from "react-router-dom";
import menus from "./../../config/app-menu.jsx";
import { validateRole } from "./../../composables/sessionData.js";

function NavItem({ pathParent, menu, ...props }: LinkProps) {
	const menuPath = (pathParent ?? "") + menu.path;
	const resolved = useResolvedPath(menuPath);
	const match = useMatch({ path: resolved.pathname });

	const location = useLocation();
	const match2 = matchPath({ path: menuPath, end: false }, location.pathname);

	const icon = menu.icon && <div className="menu-icon"><i className={menu.icon}></i></div>;
	const img = menu.img && <div className="menu-icon-img"><img src={menu.img} alt="" /></div>;
	const caret = (menu.children && !menu.badge) && <div className="menu-caret"></div>;
	const label = menu.label && <span className="menu-label ms-5px">{menu.label}</span>;
	const badge = menu.badge && <div className="menu-badge">{menu.badge}</div>;
	const highlight = menu.highlight && <i className="fa fa-paper-plane text-theme"></i>;
	const title = menu.title && <div className="menu-text">{menu.title} {label} {highlight}</div>;

	return (
		<div className={"menu-item" + ((match || match2) ? " active" : "") + (menu.children ? " has-sub" : "")}>			
			<NavLink className="menu-link" to={menuPath} {...props}>
				{img} {icon} {title}{caret} {badge}
			</NavLink>

			{menu.children && (
				<div className="menu-submenu">
					{menu.children.map((submenu, i) => <NavItem key={i} pathParent={menu.path} menu={submenu} />)}
				</div>
			)}			
		</div>
	);
};

class SidebarNav extends React.Component {

	constructor(props) {
		super(props);
		this.state = {
			menus: menus
		};
	}

	componentDidMount() {
		this.setState(state => {
			state.menus = state.menus.filter((menu) => validateRole(menu.allowedRoles));
			return state;
		});
	}

	render() {
		return (
			<div className="menu">
				<div className="menu-header">Navegación</div>
				{this.state.menus.map((menu, i) => <NavItem key={i} menu={menu} />)}
			</div>
		);
	}
};

export default SidebarNav;