(function() {
  'use strict';

  var body = $('body'),
      loginButton = $('.login'),
      gSignin = $('#g-signin'),
      logoutButton = $('.logout'),
      navDrawer = $('.nav-drawer'),
      drawerButton = $('.drawer-button'),
      obfuscator = $('.obfuscator'),
      itemDeleteButton = $('.item-delete-button'),
      photoDeleteButton = $('.photo-delete-button'),
      loginModal = $('.login-modal'),
      loginModalCancelButton = $('.login-modal__cancel-button');

  loginButton.click(toggleLoginModal);
  gSignin.click(googleSignin);
  logoutButton.click(logout);
  drawerButton.click(toggleNavDrawer);
  obfuscator.click(toggleNavDrawer);
  itemDeleteButton.click(deleteItem);
  photoDeleteButton.click(deletePhoto);
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

  // Prepare the AJAX POST request
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader('X-CSRFToken', $('.csrf-token').text());
      }
    }
  });

  function googleSignin(e) {
    e.preventDefault();
    // `auth2` is defined in <script/> in <head/> of base.html
    auth2.grantOfflineAccess().then(gSigninCallback);
  }

  function gSigninCallback(authResult) {
    if (authResult.code) {
      $.ajax({
        method: 'POST',
        url: '/login/google/',
        headers: {
          // Already set by Jquery by default, explicit is better though
          'X-Requested-With': 'XMLHttpRequest'
        },
        contentType: 'application/octet-stream; charset=utf-8',
        success: function(result) {
          console.log(result);
          window.location = '/';
        },
        processData: false,
        data: authResult.code
      });
    } else {
      console.log('authResult error: ' + authResult.error);
    }
  }

  // Log the user out
  function logout(e) {
    e.preventDefault();
    $.post($(e.target).attr('href'))
      .done(function(data) {
        console.log(data);
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
    $.post($(e.target).closest('a').attr('href'))
      .done(function(data) {
        console.log(data);
        window.location = '/';
      })
      .fail(function(xhr) {
        console.log('CSRF Token not valid');
        console.log(xhr.status);
      });
  }

  // Delete the ItemPhoto
  function deletePhoto(e) {
    e.preventDefault();
    $.post($(e.target).attr('href'))
      .done(function(data) {
        $(e.target).closest('.mdl-card').remove();
        console.log(data);
      })
      .fail(function(xhr) {
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
