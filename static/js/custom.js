/**
 *
 * You can write your JS code here, DO NOT touch the default style file
 * because it will make it harder for you to update.
 * 
 */

"use strict";

$('#cv').on('change',function(){
    let cv = $(this).val()
    $('#cv-label').html(cv)
})

// iziToast.success({
//     title: 'Blog',
//     message: 'Delete successfully',
//     position: 'topRight'
//   });