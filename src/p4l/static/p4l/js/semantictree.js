/* semantictree.js : We suppose that jquery, jquery ui, tag-it, jstree and smoothness theme have been loaded */

var semantictree_config = {
        cancel_button_text : "Cancel",
        ok_button_text : "Ok",
}

function init_autocomplete()
{
    // Wikipedia search management (new tag)
    $(".semantic-tree").autocomplete({
        source: function( request, response ) {
            // We use "this" because there can be several autocomplete in the same form.
            // this.element[0] is the input.
            var the_input = $(this.element[0]);
            var reg = the_input.val();
            var url = the_input.attr("data-url");
            var query = the_input.attr("data-query");
            $.ajax({
                url : url,
                data: {
                    query: query,
                    $reg: '"'+reg+'"',
                    $language: '"fr"'
                },
                headers: { 
                    Accept: "application/sparql-results+json;charset=UTF-8"
                },
                success: function( data ) {
                    // build response
                    response( $.map( data["results"]["bindings"], function( item ) {
                        // If acronym
                        var s = (("acro" in item)?(item["acro"]["value"] + ". "):"") + item["label"]["value"];
                        return {
                            label: s,
                            value: s + " (" + item["uri"]["value"] + ")"
                        }
                    }));
                }
            });
        },
        select: function(event, ui) {
            // We use "this" because there can be several autocomplete in the same form.
            // this is the input.
            // addSubjectText is like "label (uri)" so we get the chars inner the last brackets
            uri = ui.item.value.match(/\(([^)]*)\)[^(]*$/)[1]
            // First we update the uri/label dict
            angular.element(this).scope().updateUriLabelDict(uri, ui.item.label);
            // Angular does not listen to val() event so we update the model value manually:
            angular.element(this).controller('ngModel').$setViewValue(uri);
            angular.element(this).scope().$apply();
        },
        minLength: 2
    });
}


function init_browse() {

    $( ".dialog-link" ).each(function() {
        var input_name = this.id.substr(12);

        // Link to open the dialog
        $( '#dialog-link-'+input_name ).click(function( event ) {
            event.preventDefault();
            var input_name = this.id.substr(12);
            $( '#dialog-'+input_name ).dialog( "open" );
        });

        $( '#dialog-'+input_name ).dialog({
            autoOpen: false,
            width: 600,
            height: "auto",
            //maxHeight: 800,
            resizable: true,
            position: {my: "left top", at:"left bottom+5", of:$("#dialog-link-container-"+input_name), collision: 'none'},
            open: function(event, ui) {
                // this is the span with class="dialog" and id="dialog-inputname"
                var input_name = this.id.substr(7);
                var url = $("#id_"+input_name).attr("data-url");
                var root_query = $("#id_"+input_name).attr("data-root-query");
                var childs_query = $("#id_"+input_name).attr("data-childs-query");
                var child_count_query = $("#id_"+input_name).attr("data-child-count-query");
                // We load the tree only once
                if(!$('#term-tree-'+input_name).hasClass("jstree")){
                    $('#term-tree-'+input_name).jstree({
                        themes: {
                            dots: true,
                            icons: true
                        },
                        core: {
                            data: {
                                url : url,
                                data: function(node){
                                    var res = {};
                                    if(node.original && node.original.metadata) {
                                        res.query = childs_query;
                                        res.$root = node.original.metadata.uri;
                                    }
                                    else{
                                        res.query = root_query;
                                    }
                                    res.$language = '"fr"';
                                    return res;
                                },
                                headers: { 
                                    Accept: "application/sparql-results+json;charset=UTF-8"
                                },
                                dataFilter: function(data) {
                                    var json_obj = JSON.parse(data);
                                    var b = json_obj["results"]["bindings"];
                                    var mytree = [];
                                    var l = b.length;
                                    for(var i=0;i<l;i++){
                                        var uri = b[i]["uri"]["value"];
                                        // We test if the uri has childs.
                                        var nb = 0;
                                        if(child_count_query && child_count_query!=""){
                                            $.ajax({
                                                url:url,
                                                data:{
                                                    query: child_count_query,
                                                    $root: "<"+uri+">"
                                                },
                                                headers: {
                                                    Accept: "application/sparql-results+json;charset=UTF-8"
                                                },
                                                async: false,
                                                success:function(json_count){
                                                    nb = parseInt(json_count["results"]["bindings"][0]["nb"]["value"]);
                                                }
                                            });
                                        }
                                        // Test if the node is a collection and not selectable
                                        var attr = {'rel':'default'};
                                        if("type" in b[i]){
                                            type_uri = b[i]["type"]["value"];
                                            // type uri in kind of http://www[...]#Concept or http://www[...]#Collection
                                            if(type_uri.substr(type_uri.indexOf("#") + 1).toLowerCase()=="collection"){
                                                attr = {'rel':'leaf'};
                                            }
                                        }
                                        // If acronym :
                                        var s = (("acro" in b[i])?(b[i]["acro"]["value"] + ". "):"") + b[i]["label"]["value"];
                                        // nb of child > 0 : state closed if yes, no state if not.
                                        if(nb>0){
                                            mytree.push({
                                                text : s + " (" + nb + ") ",
                                                state : {
                                                    opened: false,
                                                },
                                                children: true,
                                                metadata : {uri: "<"+uri+">", label:s},
                                                li_attr: attr
                                            });
                                        }
                                        else{
                                            mytree.push({
                                                text : s,
                                                metadata : {uri: "<"+uri+">", label:s},
                                                li_attr: attr
                                            });
                                        }
                                    }
                                    return JSON.stringify(mytree);
                                },
                                error: function() {
                                    $(".jstree-loading").removeClass("jstree-loading").addClass("jstree-error").html("Error when loading tree");
                                }
                            },
                        },
                        types : {
                            types: {
                                "leaf" : {
                                    'hover_node' : false,
                                    'select_node': function () {return false;}
                                }
                            }
                        },
                        plugins : [ "types"]
                    });
                }
            },
            buttons: [
                      {
                          text: semantictree_config.ok_button_text,
                          click: function() {
                              // this is the span with id="dialog-inputname"
                              var input_name = this.id.substr(7);
                              selected = $.jstree.reference($('#term-tree-'+input_name)).get_selected(true);
                              if(selected.length) {
                                  selected_node = $(selected[0]);
                                  // Update text input : val() if classical input, add tag to tagit instance if necessary
                                  if($('#id_'+input_name).hasClass("semantic-tree-tagit")){
                                      // #TODO : update when we add tag-it for real
                                      $('#id_'+input_name).tagit("createTag", selected_node.attr('original').metadata.label);
                                  }
                                  else{
                                      // First we update the uri/label dict
                                      uri = selected_node.attr('original').metadata.uri;
                                      // We remove the <> from the uri
                                      uri = uri.slice(1,-1);
                                      label = selected_node.attr('original').metadata.label;
                                      angular.element($('#id_'+input_name)[0]).scope().updateUriLabelDict(uri, label);
                                      // Angular does not listen to val() event so we update the model value manually:
                                      angular.element($('#id_'+input_name)[0]).controller('ngModel').$setViewValue(uri);
                                      angular.element($('#id_'+input_name)[0]).scope().$apply();
                                      // And update the text field val
                                      $('#id_'+input_name).val(label + " (" + uri + ")");
                                  }
                                  //$('#thesaurus_tree').data('term_tree_node',selected_node.data('term_tree_node'));
                                  //$('#thesaurus_tree').val(selected_node.data('term_tree_node').id).trigger('change');                        
                              }
                              $( this ).dialog( "close" );
                          }
                      },
                      {
                          text: semantictree_config.cancel_button_text,
                          click: function() {
                              $(this).dialog( "close" );
                          }
                      }
                      ]
        });
    });
}

function init_tagit_autocomplete()
{
    // Semantic search management with tag-it feature
    /*$(".semantic-tree-tagit").tagit({
    	tagSource: function(request, response) {
        	// We use "this" because there can be several autocomplete in the same form.
        	// this.element[0] is the input.
            var url = $(this.element[0]).attr("data-url");
            var query = $(this.element[0]).attr("data-query");
            $.ajax({
            	url : url,
                data: {
                	query: query,
                	$reg: '"'+request.term+'"',
                	$language: '"fr"'
                },
            	headers: { 
                    Accept: "application/sparql-results+json;charset=UTF-8"
            	},
                success: function( data ) {
                	response( $.map( data["results"]["bindings"], function( item ) {
                		return {
                			label: item["label"]["value"],
                			value: item["uri"]["value"]
                		}
                    }));
                }
            });
        },
        allowSpaces: true
    });*/
}


$(document).ready(function(){
    init_autocomplete();
    init_browse();
    init_tagit_autocomplete();
    // Close dialogs on click/focus. focus can not be listened because of obvious loop problem.
    $(document).on('click', '.semantic-tree', function() {
        $(".dialog").dialog("close");
        if(!$(this).is(":focus")){
            $(this).focus();
        }
    });
});