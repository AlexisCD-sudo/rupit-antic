'use strict';
var theme = {
  /**
   * Theme's components/functions list
   * Comment out or delete the unnecessary component.
   * Some components have dependencies (plugins).
   * 
   */
  init: function () {
	
 /**
   * sb
   */
   // theme.subMenu();
	//theme.offCanvas();
	  theme.plyr();
   theme.pageProgress();
	

// theme.themeModeSwitch();
// theme.stickyNavbar();
	theme.gallery();
	// theme.carousel();
	//	theme.parallax();

  },

  /**
   * Sub Menus
   * Enables multilevel dropdown
   */
  subMenu: () => {
    (function($bs) {
      const CLASS_NAME = 'has-child-dropdown-show';
      $bs.Dropdown.prototype.toggle = function(_original) {
          return function() {
              document.querySelectorAll('.' + CLASS_NAME).forEach(function(e) {
                  e.classList.remove(CLASS_NAME);
              });
              let dd = this._element.closest('.dropdown').parentNode.closest('.dropdown');
              for (; dd && dd !== document; dd = dd.parentNode.closest('.dropdown')) {
                  dd.classList.add(CLASS_NAME);
              }
              return _original.call(this);
          }
      }($bs.Dropdown.prototype.toggle);
      document.querySelectorAll('.dropdown').forEach(function(dd) {
          dd.addEventListener('hide.bs.dropdown', function(e) {
              if (this.classList.contains(CLASS_NAME)) {
                  this.classList.remove(CLASS_NAME);
                  e.preventDefault();
              }
              e.stopPropagation();
          });
      });
    })(bootstrap);
  },
  
 /**
   * Offcanvas
   */
  offCanvas: () => {
    var navbar = document.querySelector(".navbar");
    if (navbar == null) return;
    
    const searchOffcanvas = document.getElementById('offcanvas-search');
    
    if(searchOffcanvas != null) {
      searchOffcanvas.addEventListener('shown.bs.offcanvas', function () {
        document.getElementById("search-form").focus();
      });
    }
  },


    /**
   * Plyr
   * Enables media player
   * Requires assets/js/vendor/plyr.js
   */
  plyr: () => {
    var players = Plyr.setup('.player', {
      loadSprite: true,
    });
  },
  
  
 /**
   * Page Progress
   * Shows page progress on the bottom right corner of pages
   */
  pageProgress: () => {
    var progressWrap = document.querySelector('.progress-wrap');
    if(progressWrap != null) {
      var progressPath = document.querySelector('.progress-wrap path');
      var pathLength = progressPath.getTotalLength();
      var offset = 50;
      progressPath.style.transition = progressPath.style.WebkitTransition = 'none';
      progressPath.style.strokeDasharray = pathLength + ' ' + pathLength;
      progressPath.style.strokeDashoffset = pathLength;
      progressPath.getBoundingClientRect();
      progressPath.style.transition = progressPath.style.WebkitTransition = 'stroke-dashoffset 10ms linear';
      window.addEventListener("scroll", function(event) {
        var scroll = document.body.scrollTop || document.documentElement.scrollTop;
        var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        var progress = pathLength - (scroll * pathLength / height);
        progressPath.style.strokeDashoffset = progress;
        var scrollElementPos = document.body.scrollTop || document.documentElement.scrollTop;
        if(scrollElementPos >= offset) {
          progressWrap.classList.add("active-progress")
        } else {
          progressWrap.classList.remove("active-progress")
        }
      });
      progressWrap.addEventListener('click', function(e) {
        e.preventDefault();
        window.scroll({
          top: 0, 
          left: 0,
          behavior: 'smooth'
        });
      });
    }
  },


  
  
 /**
 * Theme Mode Switch
 * Switch betwen light/dark mode. The chosen mode is saved to browser's local storage
*/
 themeModeSwitch: () => {


       'use strict'

  const getStoredTheme = () => localStorage.getItem('theme')
  const setStoredTheme = theme => localStorage.setItem('theme', theme)

  const getPreferredTheme = () => {
    const storedTheme = getStoredTheme()
    if (storedTheme) {
      return storedTheme
    }

    // Set default theme to 'light'.
    // Possible options: 'dark' or system color mode (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')
    return 'light'
  }

  const setTheme = theme => {
    if (theme === 'auto' && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      document.documentElement.setAttribute('data-bs-theme', 'dark')
    } else {
      document.documentElement.setAttribute('data-bs-theme', theme)
    }
  }

  setTheme(getPreferredTheme())

  const showActiveTheme = (theme) => {
    const themeSwitcher = document.querySelector('[data-bs-toggle="mode"]')
    const themeSwitcherCheck = themeSwitcher.querySelector('input[type="checkbox"]')

    if (!themeSwitcher) {
      return
    }

    if (theme === 'dark') {
      themeSwitcherCheck.checked = 'checked'
    } else {
      themeSwitcherCheck.checked = false
    }
  }

  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
    const storedTheme = getStoredTheme()
    if (storedTheme !== 'light' && storedTheme !== 'dark') {
      setTheme(getPreferredTheme())
    }
  })

  window.addEventListener('DOMContentLoaded', () => {
    showActiveTheme(getPreferredTheme())

    document.querySelectorAll('[data-bs-toggle="mode"]')
      .forEach(toggle => {
        toggle.addEventListener('click', () => {
          const theme = toggle.querySelector('input[type="checkbox"]').checked === true ? 'dark' : 'light'
          setStoredTheme(theme)
          setTheme(theme)
          showActiveTheme(theme, true)
        })
      })
  })

}, 

  
/**
 * Gallery like styled lightbox component for presenting various types of media
 * @requires https://github.com/sachinchoolur/lightGallery
*/

 gallery: () => {

  let gallery = document.querySelectorAll('.gallery');

  if (gallery.length) {
    for (let i = 0; i < gallery.length; i++) {

      const thumbnails = gallery[i].dataset.thumbnails ? true : false,
            video = gallery[i].dataset.video ? true : false,
            defaultPlugins = [lgZoom, lgFullscreen],
            videoPlugin = video ? [lgVideo] : [],
            thumbnailPlugin = thumbnails ? [lgThumbnail] : [],
            plugins = [...defaultPlugins, ...videoPlugin, ...thumbnailPlugin]

      lightGallery(gallery[i], {
        selector: '.gallery-item',
        plugins: plugins,
        licenseKey: 'D4194FDD-48924833-A54AECA3-D6F8E646',
        download: false,
        autoplayVideoOnSlide: true,
        zoomFromOrigin: false,
        youtubePlayerParams: {
          modestbranding: 1,
          showinfo: 0,
          rel: 0
        },
        vimeoPlayerParams: {
          byline: 0,
          portrait: 0,
          color: '6366f1'
        }
      });
    }
  }
},


  
/**
 * Sticky Navbar
 * Enable sticky behavior of navigation bar on page scroll
*/

 stickyNavbar: () => {

  let navbar = document.querySelector('.navbar-sticky');

  if (navbar == null) return;

  let navbarClass = navbar.classList,
      navbarH = navbar.offsetHeight,
      scrollOffset = 500;

  if (navbarClass.contains('position-absolute')) {
    window.addEventListener('scroll', (e) => {
      if (e.currentTarget.pageYOffset > scrollOffset) {
        navbar.classList.add('navbar-stuck');
      } else {
        navbar.classList.remove('navbar-stuck');
      }
    });
  } else {
    window.addEventListener('scroll', (e) => {
      if (e.currentTarget.pageYOffset > scrollOffset) {
        document.body.style.paddingTop = navbarH + 'px';
        navbar.classList.add('navbar-stuck');
      } else {
        document.body.style.paddingTop = '';
        navbar.classList.remove('navbar-stuck');
      }
    });
  }

},



/**
 * Content carousel with extensive options to control behaviour and appearance
 * @requires https://github.com/nolimits4web/swiper
*/
 
/**
 * Content carousel with extensive options to control behaviour and appearance
 * Secure version: filters __proto__/constructor/prototype, validates keys (whitelist)
 */
carousel: () => {

  // small utility: forEach for NodeList
  let forEach = (array, callback, scope) => {
    for (let i = 0; i < array.length; i++) {
      callback.call(scope, i, array[i]);
    }
  };

  // reviver for JSON.parse: remove dangerous keys during parse
  function reviverRejectProto(key, value) {
    if (key === '__proto__' || key === 'constructor' || key === 'prototype') {
      return undefined;
    }
    return value;
  }

  // deep sanitizer (defence-in-depth) - removes dangerous keys that could remain
  function sanitizeObject(obj) {
    if (obj === null || typeof obj !== 'object') return;
    // use Object.keys to avoid inherited props
    for (const k of Object.keys(obj)) {
      if (k === '__proto__' || k === 'constructor' || k === 'prototype') {
        delete obj[k];
        continue;
      }
      sanitizeObject(obj[k]);
    }
  }

  // Whitelist schema: allowed top-level keys and their expected types (primitive check)
  // Extend this schema with the fields your app expects.
  const ALLOWED_SCHEMA = {
    // example common Swiper options you might accept
    slidesPerView: 'number',
    loop: 'boolean',
    speed: 'number',
    spaceBetween: 'number',
    autoplay: 'object',    // if you support autoplay object
    centeredSlides: 'boolean',
    tabs: 'boolean',
    pager: 'boolean'
  };

  // Validate and *return a new object* with only allowed keys and correct primitive types.
  // This prevents unexpected keys from being passed to Swiper.
  function validateAndFilterOptions(raw) {
    if (!raw || typeof raw !== 'object') return {};
    const filtered = Object.create(null); // map without prototype
    for (const key of Object.keys(raw)) {
      // skip any dangerous keys just in case
      if (key === '__proto__' || key === 'constructor' || key === 'prototype') continue;
      const expectedType = ALLOWED_SCHEMA[key];
      if (!expectedType) {
        // key is not in whitelist -> ignored
        continue;
      }
      const value = raw[key];
      // type check (for objects, ensure it's non-null object)
      if (expectedType === 'object') {
        if (value && typeof value === 'object') {
          // copy shallow object only (prevent prototype)
          const objCopy = Object.create(null);
          for (const k of Object.keys(value)) {
            // avoid copying dangerous keys into nested objects
            if (k === '__proto__' || k === 'constructor' || k === 'prototype') continue;
            objCopy[k] = value[k];
          }
          filtered[key] = objCopy;
        }
      } else if (typeof value === expectedType) {
        filtered[key] = value;
      } else {
        // try to coerce some reasonable types (e.g., numeric strings -> numbers)
        if (expectedType === 'number' && typeof value === 'string' && value.trim() !== '' && !isNaN(Number(value))) {
          filtered[key] = Number(value);
        } else if (expectedType === 'boolean' && typeof value === 'string') {
          const lv = value.toLowerCase();
          if (lv === 'true' || lv === 'false') filtered[key] = lv === 'true';
        }
        // otherwise ignore the key (do not throw)
      }
    }
    return filtered;
  }

  // Carousel initialisation
  let carousels = document.querySelectorAll('.swiper');
  forEach(carousels, (index, value) => {

    let userOptions = {};
    let pagerOptions;

    // parse dataset safely
    if (value.dataset && value.dataset.swiperOptions !== undefined) {
      try {
        // 1) parse with reviver to drop __proto__/constructor/prototype as it's parsed
        const parsed = JSON.parse(value.dataset.swiperOptions, reviverRejectProto);

        // 2) deep sanitize (defense in depth)
        sanitizeObject(parsed);

        // 3) validate & filter against whitelist schema -> result is safe to use
        userOptions = validateAndFilterOptions(parsed);
      } catch (err) {
        // parsing failed or invalid JSON: log and continue with defaults
        // don't throw to avoid breaking page; you may adjust to your logging system
        if (window && window.console && window.console.warn) {
          console.warn('Invalid swiperOptions JSON on .swiper element, ignoring user options.', err);
        }
        userOptions = {};
      }
    }

    // Pager (only if user explicitly requests pager: true)
    if (userOptions.pager) {
      pagerOptions = {
        pagination: {
          el: '.pagination .list-unstyled',
          clickable: true,
          bulletActiveClass: 'active',
          bulletClass: 'page-item',
          renderBullet: function (index, className) {
            return '<li class="' + className + '"><a href="#" class="page-link btn-icon btn-sm">' + (index + 1) + '</a></li>';
          }
        }
      };
    }

    // Build final options safely: start from empty plain object
    // and only copy whitelisted properties we validated. This prevents prototype inheritance.
    const safeOptions = Object.assign(Object.create(null), userOptions || {}, pagerOptions || {});

    // Now initialize Swiper with safeOptions
    let swiper = new Swiper(value, safeOptions);

    // Tabs (linked content) - only if validated tabs === true
    if (userOptions.tabs) {
      swiper.on('activeIndexChange', (e) => {
        // protect against malformed slide dataset references
        try {
          const activeSlide = e.slides && e.slides[e.activeIndex];
          const previousSlide = e.slides && e.slides[e.previousIndex];
          const targetSelector = activeSlide && activeSlide.dataset && activeSlide.dataset.swiperTab;
          const previousSelector = previousSlide && previousSlide.dataset && previousSlide.dataset.swiperTab;
          const targetTab = targetSelector ? document.querySelector(targetSelector) : null;
          const previousTab = previousSelector ? document.querySelector(previousSelector) : null;
          if (previousTab) previousTab.classList.remove('active');
          if (targetTab) targetTab.classList.add('active');
        } catch (ex) {
          // swallow errors to avoid breaking slider on malformed data
          if (window && window.console && window.console.warn) {
            console.warn('Error handling swiper tabs event', ex);
          }
        }
      });
    }

  });

}, // end carousel



/**
 * Mouse move parallax effect
 * @requires https://github.com/wagerfield/parallax
*/


 parallax: () => {

  let element = document.querySelectorAll('.parallax');

  for (let i = 0; i < element.length; i++) {
    let parallaxInstance = new Parallax(element[i]);
  }

},





}
theme.init();