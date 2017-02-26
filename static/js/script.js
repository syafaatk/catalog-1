(function() {
  'use strict';

  var body = $('body'),
      logoutButton = $('.logout'),
      navDrawer = $('.nav-drawer'),
      drawerButton = $('.drawer-button'),
      obfuscator = $('.obfuscator');

  logoutButton.click(logout);
  drawerButton.click(triggerNavDrawer);
  obfuscator.click(triggerNavDrawer);

  // Check screen resolution changes to toggle nav drawer
  $(window).resize(function() {
    var width = $(window).width(),
        smScreen = 576;
    if (width > smScreen && body.hasClass('has-nav-drawer')) {
      triggerNavDrawer();
    }
  });

  // Log the user out
  function logout(e) {
    e.preventDefault();
    $.ajax({
      method: 'POST',
      url: $(e.target).attr('href')
    })
      .done(function(data) {
        window.location = '/';
      });
  }

  // Slide out the navigation drawer
  function triggerNavDrawer(e) {
    var expandedAria = true ? drawerButton.attr('aria-expanded') == "false" : false;
    var ndHiddenAria = true ? navDrawer.attr('aria-hidden') == "false" : false;
    drawerButton.attr('aria-expanded', expandedAria);
    navDrawer.attr('aria-hidden', ndHiddenAria);
    obfuscator.toggleClass('is-visible');
    navDrawer.toggleClass('is-visible');
    body.toggleClass('has-nav-drawer');
  }
})();
