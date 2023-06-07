import React from 'react';
import { AppSettings } from './config/app-settings.js';
import { slideToggle } from './composables/slideToggle.js';
import Header from './components/header/header.jsx';
import Sidebar from './components/sidebar/sidebar.jsx';
import Content from './components/content/content.jsx';

class App extends React.Component {
	constructor(props) {
		super(props);

		this.toggleAppSidebarMinify = (e) => {
			e.preventDefault();
			this.setState(state => ({
				appSidebarMinify: !this.state.appSidebarMinify
			}));
			if (localStorage) {
				localStorage.appSidebarMinify = !this.state.appSidebarMinify;
			}
		}
		this.toggleAppSidebarMobile = (e) => {
			e.preventDefault();
			this.setState(state => ({
				appSidebarMobileToggled: !this.state.appSidebarMobileToggled
			}));
		}
		this.handleSetAppSidebarNone = (value) => {
			this.setState(state => ({
				appSidebarNone: value
			}));
		}
		this.handleSetAppSidebarMinified = (value) => {
			this.setState(state => ({
				appSidebarMinify: value
			}));
		}
		this.handleSetAppSidebarWide = (value) => {
			this.setState(state => ({
				appSidebarWide: value
			}));
		}
		this.handleSetAppSidebarLight = (value) => {
			this.setState(state => ({
				appSidebarLight: value
			}));
		}
		this.handleSetAppSidebarTransparent = (value) => {
			this.setState(state => ({
				appSidebarTransparent: value
			}));
		}
		this.handleSetAppSidebarSearch = (value) => {
			this.setState(state => ({
				appSidebarSearch: value
			}));
		}
		this.handleSetAppSidebarFixed = (value) => {
			if (value === true && !this.state.appHeaderFixed) {
				alert('Default Header with Fixed Sidebar option is not supported. Proceed with Fixed Header with Fixed Sidebar.');
				this.setState(state => ({
					appHeaderFixed: true
				}));
				if (localStorage) {
					localStorage.appHeaderFixed = true;
				}
			}
			this.setState(state => ({
				appSidebarFixed: value
			}));
			if (localStorage) {
				localStorage.appSidebarFixed = value;
			}
		}
		this.handleSetAppSidebarGrid = (value) => {
			this.setState(state => ({
				appSidebarGrid: value
			}));
			if (localStorage) {
				localStorage.appSidebarGrid = value;
			}
		}

		this.toggleAppSidebarEnd = (e) => {
			e.preventDefault();
			this.setState(state => ({
				appSidebarEndToggled: !this.state.appSidebarEndToggled
			}));
		}
		this.toggleAppSidebarEndMobile = (e) => {
			e.preventDefault();
			this.setState(state => ({
				appSidebarEndMobileToggled: !this.state.appSidebarEndMobileToggled
			}));
		}
		this.handleSetAppSidebarEnd = (value) => {
			this.setState(state => ({
				appSidebarEnd: value
			}));
		}

		this.handleSetAppContentNone = (value) => {
			this.setState(state => ({
				appContentNone: value
			}));
		}
		this.handleSetAppContentClass = (value) => {
			this.setState(state => ({
				appContentClass: value
			}));
		}
		this.handleSetAppContentFullHeight = (value) => {
			this.setState(state => ({
				appContentFullHeight: value
			}));
		}

		this.handleSetAppHeaderNone = (value) => {
			this.setState(state => ({
				appHeaderNone: value
			}));
		}
		this.handleSetAppHeaderFixed = (value) => {
			if (value === false && this.state.appSidebarFixed) {
				alert('Default Header with Fixed Sidebar option is not supported. Proceed with Default Header with Default Sidebar.');
				this.setState(state => ({
					appSidebarFixed: false
				}));
				if (localStorage) {
					localStorage.appSidebarFixed = false;
				}
			}
			this.setState(state => ({
				appHeaderFixed: value
			}));
			if (localStorage) {
				localStorage.appHeaderFixed = value;
			}
		}
		this.handleSetAppHeaderInverse = (value) => {
			this.setState(state => ({
				appHeaderInverse: value
			}));
			if (localStorage) {
				localStorage.appHeaderInverse = value;
			}
		}
		this.handleSetAppHeaderMegaMenu = (value) => {
			this.setState(state => ({
				appHeaderMegaMenu: value
			}));
		}
		this.handleSetAppHeaderLanguageBar = (value) => {
			this.setState(state => ({
				appHeaderLanguageBar: value
			}));
		}

		this.handleSetAppTopMenu = (value) => {
			this.setState(state => ({
				appTopMenu: value
			}));
		}
		this.toggleAppTopMenuMobile = (e) => {
			e.preventDefault();

			slideToggle(document.querySelector('.app-top-menu'));
		}
		this.handleSetAppSidebarTwo = (value) => {
			this.setState(state => ({
				appSidebarTwo: value
			}));
			this.setState(state => ({
				appSidebarEndToggled: value
			}));
		}
		this.handleSetAppBoxedLayout = (value) => {
			if (value === true) {
				document.body.classList.add('boxed-layout');
			} else {
				document.body.classList.remove('boxed-layout');
			}
		}
		this.handleSetAppDarkMode = (value) => {
			if (value === true) {
				document.body.classList.add('dark-mode');
			} else {
				document.body.classList.remove('dark-mode');
			}
			this.setState(state => ({ appDarkMode: value }));
			this.handleSetColor();
			if (localStorage) {
				localStorage.appDarkMode = value;
			}
		}
		this.handleSetAppGradientEnabled = (value) => {
			this.setState(state => ({
				appGradientEnabled: value
			}));
			if (localStorage) {
				localStorage.appGradientEnabled = value;
			}
		}
		this.handleSetFont = () => {
			this.setState(state => ({
				font: {
					family: window.getComputedStyle(document.body).getPropertyValue('--bs-body-font-family').trim(),
					size: window.getComputedStyle(document.body).getPropertyValue('--bs-body-font-size').trim(),
					weight: window.getComputedStyle(document.body).getPropertyValue('--bs-body-font-family').trim()
				}
			}));
		}
		this.handleSetColor = () => {
			this.setState(state => ({
				color: {
					componentColor: window.getComputedStyle(document.body).getPropertyValue('--app-component-color').trim(),
					componentBg: window.getComputedStyle(document.body).getPropertyValue('--app-component-bg').trim(),
					dark: window.getComputedStyle(document.body).getPropertyValue('--bs-dark').trim(),
					light: window.getComputedStyle(document.body).getPropertyValue('--bs-light').trim(),
					blue: window.getComputedStyle(document.body).getPropertyValue('--bs-blue').trim(),
					indigo: window.getComputedStyle(document.body).getPropertyValue('--bs-indigo').trim(),
					purple: window.getComputedStyle(document.body).getPropertyValue('--bs-purple').trim(),
					pink: window.getComputedStyle(document.body).getPropertyValue('--bs-pink').trim(),
					red: window.getComputedStyle(document.body).getPropertyValue('--bs-red').trim(),
					orange: window.getComputedStyle(document.body).getPropertyValue('--bs-orange').trim(),
					yellow: window.getComputedStyle(document.body).getPropertyValue('--bs-yellow').trim(),
					green: window.getComputedStyle(document.body).getPropertyValue('--bs-green').trim(),
					success: window.getComputedStyle(document.body).getPropertyValue('--bs-success').trim(),
					teal: window.getComputedStyle(document.body).getPropertyValue('--bs-teal').trim(),
					cyan: window.getComputedStyle(document.body).getPropertyValue('--bs-cyan').trim(),
					white: window.getComputedStyle(document.body).getPropertyValue('--bs-white').trim(),
					gray: window.getComputedStyle(document.body).getPropertyValue('--bs-gray').trim(),
					lime: window.getComputedStyle(document.body).getPropertyValue('--bs-lime').trim(),
					gray100: window.getComputedStyle(document.body).getPropertyValue('--bs-gray-100').trim(),
					gray200: window.getComputedStyle(document.body).getPropertyValue('--bs-gray-200').trim(),
					gray300: window.getComputedStyle(document.body).getPropertyValue('--bs-gray-300').trim(),
					gray400: window.getComputedStyle(document.body).getPropertyValue('--bs-gray-400').trim(),
					gray500: window.getComputedStyle(document.body).getPropertyValue('--bs-gray-500').trim(),
					gray600: window.getComputedStyle(document.body).getPropertyValue('--bs-gray-600').trim(),
					gray700: window.getComputedStyle(document.body).getPropertyValue('--bs-gray-700').trim(),
					gray800: window.getComputedStyle(document.body).getPropertyValue('--bs-gray-800').trim(),
					gray900: window.getComputedStyle(document.body).getPropertyValue('--bs-gray-900').trim(),
					black: window.getComputedStyle(document.body).getPropertyValue('--bs-black').trim(),
					componentColorRgb: window.getComputedStyle(document.body).getPropertyValue('--app-component-color-rgb').trim(),
					componentBgRgb: window.getComputedStyle(document.body).getPropertyValue('--app-component-bg-rgb').trim(),
					darkRgb: window.getComputedStyle(document.body).getPropertyValue('--bs-dark-rgb').trim(),
					lightRgb: window.getComputedStyle(document.body).getPropertyValue('--bs-light-rgb').trim(),
					blueRgb: window.getComputedStyle(document.body).getPropertyValue('--bs-blue-rgb').trim(),
					indigoRgb: window.getComputedStyle(document.body).getPropertyValue('--bs-indigo-rgb').trim(),
					purpleRgb: window.getComputedStyle(document.body).getPropertyValue('--bs-purple-rgb').trim(),
					pinkRgb: window.getComputedStyle(document.body).getPropertyValue('--bs-pink-rgb').trim(),
					redRgb: window.getComputedStyle(document.body).getPropertyValue('--bs-red-rgb').trim(),
					orangeRgb: window.getComputedStyle(document.body).getPropertyValue('--bs-orange-rgb').trim(),
					yellowRgb: window.getComputedStyle(document.body).getPropertyValue('--bs-yellow-rgb').trim(),
					greenRgb: window.getComputedStyle(document.body).getPropertyValue('--bs-green-rgb').trim(),
					successRgb: window.getComputedStyle(document.body).getPropertyValue('--bs-success-rgb').trim(),
					tealRgb: window.getComputedStyle(document.body).getPropertyValue('--bs-teal-rgb').trim(),
					cyanRgb: window.getComputedStyle(document.body).getPropertyValue('--bs-cyan-rgb').trim(),
					whiteRgb: window.getComputedStyle(document.body).getPropertyValue('--bs-white-rgb').trim(),
					grayRgb: window.getComputedStyle(document.body).getPropertyValue('--bs-gray-rgb').trim(),
					limeRgb: window.getComputedStyle(document.body).getPropertyValue('--bs-lime-rgb').trim(),
					gray100Rgb: window.getComputedStyle(document.body).getPropertyValue('--bs-gray-100-rgb').trim(),
					gray200Rgb: window.getComputedStyle(document.body).getPropertyValue('--bs-gray-200-rgb').trim(),
					gray300Rgb: window.getComputedStyle(document.body).getPropertyValue('--bs-gray-300-rgb').trim(),
					gray400Rgb: window.getComputedStyle(document.body).getPropertyValue('--bs-gray-400-rgb').trim(),
					gray500Rgb: window.getComputedStyle(document.body).getPropertyValue('--bs-gray-500-rgb').trim(),
					gray600Rgb: window.getComputedStyle(document.body).getPropertyValue('--bs-gray-600-rgb').trim(),
					gray700Rgb: window.getComputedStyle(document.body).getPropertyValue('--bs-gray-700-rgb').trim(),
					gray800Rgb: window.getComputedStyle(document.body).getPropertyValue('--bs-gray-800-rgb').trim(),
					gray900Rgb: window.getComputedStyle(document.body).getPropertyValue('--bs-gray-900-rgb').trim(),
					blackRgb: window.getComputedStyle(document.body).getPropertyValue('--bs-black-rgb').trim()
				}
			}));
		}
		this.handleSetAppTheme = (value) => {
			var newTheme = 'theme-' + value;
			for (var x = 0; x < document.body.classList.length; x++) {
				if ((document.body.classList[x]).indexOf('theme-') > -1 && document.body.classList[x] !== newTheme) {
					document.body.classList.remove(document.body.classList[x]);
				}
			}
			document.body.classList.add(newTheme);

			if (localStorage && value) {
				localStorage.appTheme = value;
			}
		}

		this.state = {
			appTheme: '',
			appDarkMode: false,
			appGradientEnabled: false,

			appHeaderNone: false,
			appHeaderFixed: true,
			appHeaderInverse: false,
			appHeaderMegaMenu: false,
			appHeaderLanguageBar: false,
			hasScroll: false,
			handleSetAppHeaderNone: this.handleSetAppHeaderNone,
			handleSetAppHeaderInverse: this.handleSetAppHeaderInverse,
			handleSetAppHeaderLanguageBar: this.handleSetAppHeaderLanguageBar,
			handleSetAppHeaderMegaMenu: this.handleSetAppHeaderMegaMenu,
			handleSetAppHeaderFixed: this.handleSetAppHeaderFixed,

			appSidebarNone: false,
			appSidebarWide: false,
			appSidebarLight: false,
			appSidebarMinify: false,
			appSidebarMobileToggled: false,
			appSidebarTransparent: false,
			appSidebarSearch: false,
			appSidebarFixed: true,
			appSidebarGrid: false,
			handleSetAppSidebarNone: this.handleSetAppSidebarNone,
			handleSetAppSidebarWide: this.handleSetAppSidebarWide,
			handleSetAppSidebarLight: this.handleSetAppSidebarLight,
			handleSetAppSidebarMinified: this.handleSetAppSidebarMinified,
			handleSetAppSidebarTransparent: this.handleSetAppSidebarTransparent,
			handleSetAppSidebarSearch: this.handleSetAppSidebarSearch,
			handleSetAppSidebarFixed: this.handleSetAppSidebarFixed,
			handleSetAppSidebarGrid: this.handleSetAppSidebarGrid,
			toggleAppSidebarMinify: this.toggleAppSidebarMinify,
			toggleAppSidebarMobile: this.toggleAppSidebarMobile,

			appContentNone: false,
			appContentClass: '',
			appContentFullHeight: false,
			handleSetAppContentNone: this.handleSetAppContentNone,
			handleSetAppContentClass: this.handleSetAppContentClass,
			handleSetAppContentFullHeight: this.handleSetAppContentFullHeight,

			appTopMenu: false,
			appTopMenuMobileToggled: false,
			toggleAppTopMenuMobile: this.toggleAppTopMenuMobile,
			handleSetAppTopMenu: this.handleSetAppTopMenu,

			appSidebarTwo: false,
			handleSetAppSidebarTwo: this.handleSetAppSidebarTwo,

			appSidebarEnd: false,
			appSidebarEndToggled: false,
			appSidebarEndMobileToggled: false,
			toggleAppSidebarEnd: this.toggleAppSidebarEnd,
			toggleAppSidebarEndMobile: this.toggleAppSidebarEndMobile,
			handleSetAppSidebarEnd: this.handleSetAppSidebarEnd,

			handleSetAppBoxedLayout: this.handleSetAppBoxedLayout,
			handleSetAppDarkMode: this.handleSetAppDarkMode,
			handleSetAppGradientEnabled: this.handleSetAppGradientEnabled,
			handleSetAppTheme: this.handleSetAppTheme,

			handleSetColor: this.handleSetColor,

			font: {
				family: window.getComputedStyle(document.body).getPropertyValue('--bs-body-font-family').trim(),
				size: window.getComputedStyle(document.body).getPropertyValue('--bs-body-font-size').trim(),
				weight: window.getComputedStyle(document.body).getPropertyValue('--bs-body-font-family').trim()
			},
			color: {
				componentColor: window.getComputedStyle(document.body).getPropertyValue('--app-component-color').trim(),
				componentBg: window.getComputedStyle(document.body).getPropertyValue('--app-component-bg').trim(),
				dark: window.getComputedStyle(document.body).getPropertyValue('--bs-dark').trim(),
				light: window.getComputedStyle(document.body).getPropertyValue('--bs-light').trim(),
				blue: window.getComputedStyle(document.body).getPropertyValue('--bs-blue').trim(),
				indigo: window.getComputedStyle(document.body).getPropertyValue('--bs-indigo').trim(),
				purple: window.getComputedStyle(document.body).getPropertyValue('--bs-purple').trim(),
				pink: window.getComputedStyle(document.body).getPropertyValue('--bs-pink').trim(),
				red: window.getComputedStyle(document.body).getPropertyValue('--bs-red').trim(),
				orange: window.getComputedStyle(document.body).getPropertyValue('--bs-orange').trim(),
				yellow: window.getComputedStyle(document.body).getPropertyValue('--bs-yellow').trim(),
				green: window.getComputedStyle(document.body).getPropertyValue('--bs-green').trim(),
				success: window.getComputedStyle(document.body).getPropertyValue('--bs-success').trim(),
				teal: window.getComputedStyle(document.body).getPropertyValue('--bs-teal').trim(),
				cyan: window.getComputedStyle(document.body).getPropertyValue('--bs-cyan').trim(),
				white: window.getComputedStyle(document.body).getPropertyValue('--bs-white').trim(),
				gray: window.getComputedStyle(document.body).getPropertyValue('--bs-gray').trim(),
				lime: window.getComputedStyle(document.body).getPropertyValue('--bs-lime').trim(),
				gray100: window.getComputedStyle(document.body).getPropertyValue('--bs-gray-100').trim(),
				gray200: window.getComputedStyle(document.body).getPropertyValue('--bs-gray-200').trim(),
				gray300: window.getComputedStyle(document.body).getPropertyValue('--bs-gray-300').trim(),
				gray400: window.getComputedStyle(document.body).getPropertyValue('--bs-gray-400').trim(),
				gray500: window.getComputedStyle(document.body).getPropertyValue('--bs-gray-500').trim(),
				gray600: window.getComputedStyle(document.body).getPropertyValue('--bs-gray-600').trim(),
				gray700: window.getComputedStyle(document.body).getPropertyValue('--bs-gray-700').trim(),
				gray800: window.getComputedStyle(document.body).getPropertyValue('--bs-gray-800').trim(),
				gray900: window.getComputedStyle(document.body).getPropertyValue('--bs-gray-900').trim(),
				black: window.getComputedStyle(document.body).getPropertyValue('--bs-black').trim(),
				componentColorRgb: window.getComputedStyle(document.body).getPropertyValue('--app-component-color-rgb').trim(),
				componentBgRgb: window.getComputedStyle(document.body).getPropertyValue('--app-component-bg-rgb').trim(),
				darkRgb: window.getComputedStyle(document.body).getPropertyValue('--bs-dark-rgb').trim(),
				lightRgb: window.getComputedStyle(document.body).getPropertyValue('--bs-light-rgb').trim(),
				blueRgb: window.getComputedStyle(document.body).getPropertyValue('--bs-blue-rgb').trim(),
				indigoRgb: window.getComputedStyle(document.body).getPropertyValue('--bs-indigo-rgb').trim(),
				purpleRgb: window.getComputedStyle(document.body).getPropertyValue('--bs-purple-rgb').trim(),
				pinkRgb: window.getComputedStyle(document.body).getPropertyValue('--bs-pink-rgb').trim(),
				redRgb: window.getComputedStyle(document.body).getPropertyValue('--bs-red-rgb').trim(),
				orangeRgb: window.getComputedStyle(document.body).getPropertyValue('--bs-orange-rgb').trim(),
				yellowRgb: window.getComputedStyle(document.body).getPropertyValue('--bs-yellow-rgb').trim(),
				greenRgb: window.getComputedStyle(document.body).getPropertyValue('--bs-green-rgb').trim(),
				successRgb: window.getComputedStyle(document.body).getPropertyValue('--bs-success-rgb').trim(),
				tealRgb: window.getComputedStyle(document.body).getPropertyValue('--bs-teal-rgb').trim(),
				cyanRgb: window.getComputedStyle(document.body).getPropertyValue('--bs-cyan-rgb').trim(),
				whiteRgb: window.getComputedStyle(document.body).getPropertyValue('--bs-white-rgb').trim(),
				grayRgb: window.getComputedStyle(document.body).getPropertyValue('--bs-gray-rgb').trim(),
				limeRgb: window.getComputedStyle(document.body).getPropertyValue('--bs-lime-rgb').trim(),
				gray100Rgb: window.getComputedStyle(document.body).getPropertyValue('--bs-gray-100-rgb').trim(),
				gray200Rgb: window.getComputedStyle(document.body).getPropertyValue('--bs-gray-200-rgb').trim(),
				gray300Rgb: window.getComputedStyle(document.body).getPropertyValue('--bs-gray-300-rgb').trim(),
				gray400Rgb: window.getComputedStyle(document.body).getPropertyValue('--bs-gray-400-rgb').trim(),
				gray500Rgb: window.getComputedStyle(document.body).getPropertyValue('--bs-gray-500-rgb').trim(),
				gray600Rgb: window.getComputedStyle(document.body).getPropertyValue('--bs-gray-600-rgb').trim(),
				gray700Rgb: window.getComputedStyle(document.body).getPropertyValue('--bs-gray-700-rgb').trim(),
				gray800Rgb: window.getComputedStyle(document.body).getPropertyValue('--bs-gray-800-rgb').trim(),
				gray900Rgb: window.getComputedStyle(document.body).getPropertyValue('--bs-gray-900-rgb').trim(),
				blackRgb: window.getComputedStyle(document.body).getPropertyValue('--bs-black-rgb').trim()
			}
		};
	}

	componentDidMount() {
		this.handleSetColor();
		this.handleSetFont();
		this.handleSetAppTheme(this.state.appTheme);

		if (this.state.appDarkMode) {
			this.handleSetAppDarkMode(true);
		}

		window.addEventListener('scroll', this.handleScroll);

		if (localStorage) {
			if (typeof localStorage.appTheme !== 'undefined') {
				document.body.classList.add('theme-' + localStorage.appTheme);
			}
			if (typeof localStorage.appDarkMode !== 'undefined') {
				this.handleSetAppDarkMode((localStorage.appDarkMode === 'true') ? true : false);
			}
			if (typeof localStorage.appHeaderInverse !== 'undefined') {
				this.handleSetAppHeaderInverse((localStorage.appHeaderInverse === 'true') ? true : false);
			}
			if (typeof localStorage.appGradientEnabled !== 'undefined') {
				this.handleSetAppGradientEnabled((localStorage.appDarkMode === 'true') ? true : false);
			}
			if (typeof localStorage.appSidebarGrid !== 'undefined') {
				this.handleSetAppSidebarGrid((localStorage.appSidebarGrid === 'true') ? true : false);
			}
			if (typeof localStorage.appSidebarMinify !== 'undefined') {
				this.handleSetAppSidebarMinified((localStorage.appSidebarMinify === 'true') ? true : false);
			}
			if (typeof localStorage.appSidebarFixed !== 'undefined') {
				this.handleSetAppSidebarFixed((localStorage.appSidebarFixed === 'true') ? true : false);
			}
			if (typeof localStorage.appHeaderFixed !== 'undefined') {
				this.handleSetAppHeaderFixed((localStorage.appHeaderFixed === 'true') ? true : false);
			}
		}
	}

	componentWillUnmount() {
		window.removeEventListener('scroll', this.handleScroll)
	}

	handleScroll = () => {
		if (window.scrollY > 0) {
			this.setState(state => ({
				hasScroll: true
			}));
		} else {
			this.setState(state => ({
				hasScroll: true
			}));
		}

		const elm = document.getElementsByClassName('nvtooltip');

		for (let i = 0; i < elm.length; i++) {
			elm[i].classList.add('d-none');
		}
	}

	render() {
		return (
			<AppSettings.Provider value={this.state}>
				<div className={
					'app ' +
					(this.state.appGradientEnabled ? 'app-gradient-enabled ' : '') +
					(this.state.appHeaderNone ? 'app-without-header ' : '') +
					(this.state.appHeaderFixed && !this.state.appHeaderNone ? 'app-header-fixed ' : '') +
					(this.state.appSidebarFixed ? 'app-sidebar-fixed ' : '') +
					(this.state.appSidebarNone ? 'app-without-sidebar ' : '') +
					(this.state.appSidebarEnd ? 'app-with-end-sidebar ' : '') +
					(this.state.appSidebarWide ? 'app-with-wide-sidebar ' : '') +
					(this.state.appSidebarLight ? 'app-with-light-sidebar ' : '') +
					(this.state.appSidebarMinify ? 'app-sidebar-minified ' : '') +
					(this.state.appSidebarMobileToggled ? 'app-sidebar-mobile-toggled ' : '') +
					(this.state.appTopMenu ? 'app-with-top-menu ' : '') +
					(this.state.appContentFullHeight ? 'app-content-full-height ' : '') +
					(this.state.appSidebarTwo ? 'app-with-two-sidebar ' : '') +
					(this.state.appSidebarEndToggled ? 'app-sidebar-end-toggled ' : '') +
					(this.state.appSidebarEndMobileToggled ? 'app-sidebar-end-mobile-toggled ' : '') +
					(this.state.hasScroll ? 'has-scroll ' : '')
				}>
					{!this.state.appHeaderNone && (<Header />)}
					{!this.state.appSidebarNone && (<Sidebar />)}
					{!this.state.appContentNone && (<Content />)}
				</div>
			</AppSettings.Provider>
		);
	}
};

export default App;