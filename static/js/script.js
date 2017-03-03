(function() {
  'use strict';

  var body = $('body'),
      logoutButton = $('.logout'),
      navDrawer = $('.nav-drawer'),
      drawerButton = $('.drawer-button'),
      obfuscator = $('.obfuscator'),
      itemDeleteButton = $('.item-delete-button'),
      loginModal = $('.login-modal'),
      loginModalCancelButton = $('.login-modal__cancel-button');

  logoutButton.click(logout);
  drawerButton.click(toggleNavDrawer);
  obfuscator.click(toggleNavDrawer);
  itemDeleteButton.click(deleteItem);
  loginModalCancelButton.click(toggleLoginModal);
  loginModal.keydown(toggleLoginModalByKeyboard);

  // Check screen changes to hide nav drawer
  $(window).resize(function() {
    var width = $(window).width(),
        smScreen = 576;
    if (width > smScreen && body.hasClass('has-nav-drawer')) {
      toggleNavDrawer();
    }
  });

  // Preset the AJAX POST request
  function presetAJAX(CSRFToken) {
    $.ajaxSetup({
      beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader('X-CSRFToken', CSRFToken);
        }
      }
    });
  }

  // Log the user out
  function logout(e) {
    e.preventDefault();
    var elem = $(e.target),
        CSRFToken = elem.data('csrfToken'),
        url = elem.attr('href');
    presetAJAX(CSRFToken);
    $.ajax({
      method: 'POST',
      url: url
    })
      .done(function(data) {
        window.location = '/';
      })
      .fail(function(data) {
        console.log('CSRF Token not valid');
      });
  }

  // Slide out the navigation drawer
  function toggleNavDrawer(e) {
    var expandedAria = true ? drawerButton.attr('aria-expanded') == "false" : false;
    var hiddenAria = true ? navDrawer.attr('aria-hidden') == "false" : false;
    drawerButton.attr('aria-expanded', expandedAria);
    navDrawer.attr('aria-hidden', hiddenAria);
    obfuscator.toggleClass('is-visible');
    navDrawer.toggleClass('is-visible');
    body.toggleClass('has-nav-drawer');
  }

  // Delete the item
  function deleteItem(e) {
    e.preventDefault();
    var elem = $(e.target),
        CSRFToken = elem.data('csrfToken'),
        url = elem.attr('href');
    presetAJAX(CSRFToken);
    $.ajax({
      method: 'POST',
      url: url
    })
      .done(function(data) {
        window.location = '/';
      })
      .fail(function(xhr) {
        console.log('CSRF Token not valid');
        console.log(xhr);
        console.log(xhr.status);
      });
  }

  // Pop up the login modal.
  function toggleLoginModal() {
    var hiddenAria = true ? loginModal.attr('aria-hidden') == 'false' : false;
    loginModal.attr('aria-hidden', hiddenAria);
    loginModal.toggleClass('is-visible');
    body.toggleClass('has-modal');
    loginModal.focus();
  }

  function toggleLoginModalByKeyboard(e) {
    var esc = 27;
    if (e.which == esc) {
      e.preventDefault();
      toggleLoginModal();
    }
  }

  // Get the anchor part of the URL.
  function getURLAnchor() {
    var anchor = window.location.hash;
    if (anchor) return anchor;
    return false;
  }

  if (getURLAnchor() == '#login') {
    toggleLoginModal();
  }
})();
