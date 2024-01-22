"use strict";

$("select").selectric();
$.uploadPreview({
  input_field: "#avatar-upload",   // Default: .image-upload
  preview_box: "#image-preview",  // Default: .image-preview
  label_field: "#avatar-label",    // Default: .image-label
  label_default: "Choose File",   // Default: Choose File
  label_selected: "Change File",  // Default: Change File
  no_label: false,                // Default: false
  success_callback: null          // Default: null
});
$.uploadPreview({
  input_field: "#banner-upload",   // Default: .image-upload
  preview_box: "#image-preview2",  // Default: .image-preview
  label_field: "#banner-label",    // Default: .image-label
  label_default: "Choose File",   // Default: Choose File
  label_selected: "Change File",  // Default: Change File
  no_label: false,                // Default: false
  success_callback: null          // Default: null
});
$.uploadPreview({
  input_field: "#post-upload",   // Default: .image-upload
  preview_box: "#image-preview3",  // Default: .image-preview
  label_field: "#post-label",    // Default: .image-label
  label_default: "Choose File",   // Default: Choose File
  label_selected: "Change File",  // Default: Change File
  no_label: false,                // Default: false
  success_callback: null          // Default: null
});
$.uploadPreview({
  input_field: "#edit-post-upload",   // Default: .image-upload
  preview_box: "#image-preview4",  // Default: .image-preview
  label_field: "#edit-post-label",    // Default: .image-label
  label_default: "Choose File",   // Default: Choose File
  label_selected: "Change File",  // Default: Change File
  no_label: false,                // Default: false
  success_callback: null          // Default: null
});
$.uploadPreview({
  input_field: "#icon-upload",   // Default: .image-upload
  preview_box: "#image-preview5",  // Default: .image-preview
  label_field: "#icon-label",    // Default: .image-label
  label_default: "Choose File",   // Default: Choose File
  label_selected: "Change File",  // Default: Change File
  no_label: false,                // Default: false
  success_callback: null          // Default: null
});
$(".inputtags").tagsinput('items');