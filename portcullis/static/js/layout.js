function toggle_form_section(event) {
    /*
     * This function toggles the corresponding sibling div of the header
     * that calls it
     */
    
    var element = $(event.target);
    element.next().toggle('slow');
}

function collapse_all() {
    /*
     * Grabs all section toggles and hides their sibling element
     */

    $('.section_toggle').next().hide();
}

function sidepane_relocate() {
    /*
     * Checks the side panes anchor and determines if the user has scrolled it 
     * off the screen at the top.  If so make the side pane "sticky" and stay with the 
     * user down the page.
     */
    
    var window_top = $(window).scrollTop();
    var div_top = $('#side_pane_anchor').offset().top;

    if (window_top > div_top)
        $('#side_pane').addClass('stick')
    else
        $('#side_pane').removeClass('stick'); 
}
