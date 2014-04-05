"use strict";
// initialize the app

var app = angular.module("recordApp", ['ngResource', 'ngRoute', 'pascalprecht.translate']);

app.constant('p4lConfig', {
    routeEvent: ['$locationChangeStart', '$stateChangeStart']
});

app.config(function($locationProvider) {
    $locationProvider.html5Mode(true);
});

app.service("Api", function($resource, context) {
    this.record = $resource(context.urls.record_api,
            {recordId: context.record_id},
            {
                get: {
                    method: "GET",
                    isArray: false
                },
                save:{
                    method:"PUT",
                    isArray:false,
                    headers:{'X-CSRFToken':context.csrf_token}
                } 
            });
});

app.service("RecordModel", function(Api, context) {
    if(context.record == null) {
        this.record = Api.record.get();
    }
    else {
        this.record = new Api.record(context.record);
    }
    this.uriLabels = context.uri_labels;
});


app.directive('objectDisp', ['$compile', '$http', '$templateCache', 'context', function($compile, $http, $templateCache, context) {

    var getTemplate = function(templateName) {
        var templateLoader,
        templateUrl = context.urls.base_static+'p4l/templates/'+templateName+'.html';
        templateLoader = $http.get(templateUrl, {cache: $templateCache});

        return templateLoader;
    }

    var linker = function(scope, element, attrs) {

        var loader = getTemplate(scope.dispTemplate);

        var promise = loader.success(function(html) {
            element.html(html);
        }).then(function (response) {
            element.replaceWith($compile(element.html())(scope));
        });
    }

    return {
        restrict: 'E',
        scope: {
            dispTemplate: "=",
            obj: "="
        },
        link: linker
    };
}]);


app.directive('objectList', function(RecordModel, context) {
    return {
        restrict: 'E',
        replace: true,
        transclude: true,
        scope: {
            list:"=objectList",
            dispTemplate: "@dispTemplate",
            formTemplate: "@formTemplate",
            objectFields: "@objectFields",
            labelFields: "@labelFields",
            sizeFields: "@sizeFields",
            table: "@table"
        },
        controller: function($scope, $element, $attrs, $transclude) {
        	
            $scope.getStaticTemplateUrl = function(templateName) {
                return context.urls.base_static+'p4l/templates/'+templateName+".html";
            }
            $scope.getEmptyObjectFromList = function(fieldList) {
                var res = {};
                for ( var field in fieldList) {
                    res[field] = "";
                }
                return res;
            }
        },  
        templateUrl: function(tElement, tAttrs){
        	if(tAttrs.table=="true"){
        		return context.urls.base_static+'p4l/templates/objectListTable.html'
        	}
        	else{
        		return context.urls.base_static+'p4l/templates/objectList.html'
        	}
        },
        link: function($scope, $element, $attrs) {
            
            // Setup divs table parameters
            $scope.headFields = angular.fromJson($scope.objectFields);
            $scope.headLabels = angular.fromJson($scope.labelFields);
            $scope.headSizes = angular.fromJson($scope.sizeFields);
            if($scope.headSizes==undefined){
                $scope.headSizes = [];
                var n = $scope.headFields.length;
                for(var i=0;i<n;i++){
                    $scope.headSizes.push(2);
                }
            }
            if($scope.headLabels==undefined){
                $scope.headLabels = $scope.headFields;
            }
        	
            $scope.editedObj = null;
            $scope.editedIndex = -1;
            
            $scope.getEmptyObject = function() {
                return $scope.getEmptyObjectFromList($scope.headFields);
            };

            $scope.setEditedObject = function(obj, index) {
                
                var newObj = obj;
                if(index>=0) {
                    newObj = angular.copy(obj);
                }                
                $scope.editedObj = newObj;
                $scope.editedIndex = index;
            }
            
            $scope.newEditedObject = function() {
                var newObj = $scope.getEmptyObject();
                $scope.setEditedObject(newObj, -1);
            };
            
            $scope.removeFromList = function(index) {
                if(index>=0){
                    $scope.list.splice(index, 1);
                }
                $scope.setEditedObject(null, -1);
            }
                        
            $scope.onOk = function() {

                if($scope.editedIndex >= 0) {
                    $scope.list[$scope.editedIndex] = $scope.editedObj;
                }
                else {
                    $scope.list.push($scope.editedObj);
                }
                
                $scope.setEditedObject(null, -1);
                
            }
            
            $scope.onCancel = function() {
                $scope.setEditedObject(null, -1);
            }
        }
    };
});


app.directive('addSemUri', function(RecordModel, context, $timeout){
  return {
      restrict: 'E',
      replace: true,
      transclude: true,
      scope: {
    	  listname:"@",
    	  list:"=",
    	  placeholder:"@",
      },
      templateUrl: function(tElement, tAttrs) {
          return context.urls.base_static+'p4l/templates/addSemanticUriForm.html';  
      },
      link: function($scope, $element, $attrs) {
    	  // Get queries attributes from $scope listname and context query dict
    	  var attr_dict = context.query_dicts[$scope.listname];    	  
    	  for (var k in attr_dict){
			  if (attr_dict.hasOwnProperty(k)) {
			      $scope[k] = attr_dict[k];
			  }
		  }
		  $scope.formVisible = false;
    	  // initalize autocomplete and browse thesaurus events
    	  // We have to timeout because init_browse needs the real ids and not {{ $id }}
    	  // NB : scope.apply generates bug
    	  $timeout(function(){
    		  init_autocomplete();
    		  init_browse();
          }, 0);
      },
      controller: function($scope, $element, $attrs, $transclude, RecordModel){
	    $scope.record = RecordModel.record;
	    $scope.uriLabels = RecordModel.uriLabels;
	    $scope.addUriText = '';
	    $scope.uriInDict = false;
	    
	    $scope.addUriToList = function() {
	        if($scope.addUriText.match("^http://")) {
	            $scope.list.push($scope.addUriText);
	            $scope.addUriText = '';
	        }
	    };
	    $scope.removeFromList = function(obj) {
            var i = $scope.list.indexOf(obj);
            if(i>=0){
                $scope.list.splice(i, 1);
            }
        }
	    
	    $scope.updateUriLabelDict = function(k,v) {
	        $scope.uriLabels[k] = v;
	    };
	    $scope.$watch("addUriText", function(newValue, oldValue){
	    	$scope.uriInDict = (($scope.dataquery!='') && ($scope.addUriText in $scope.uriLabels));
	    });
      }
    }
});

app.directive('simpleSemUri', function(RecordModel, context, $timeout) {
    return {
        restrict: 'E',
        replace: true,
        transclude: true,
        scope: {
            listname:"@",
            val:"=",
            placeholder:"@",
        },
        templateUrl: function(tElement, tAttrs) {
            return context.urls.base_static+'p4l/templates/simpleSemanticUriForm.html';  
        },
        link: function($scope, $element, $attrs) {
            // Get queries attributes from $scope listname and context query dict
            var attr_dict = context.query_dicts[$scope.listname];
            angular.extend($scope, attr_dict);
            $scope.formVisible = false;
            
            // initalize autocomplete and browse thesaurus events
            // We have to timeout because init_browse needs the real ids and not {{ $id }}
            // NB : scope.apply generates bug
            $timeout(function(){
                init_autocomplete();
                init_browse();
            }, 0);
        },
        controller: function($scope, $element, $attrs, $transclude, RecordModel) {
            $scope.record = RecordModel.record;
            $scope.uriLabels = RecordModel.uriLabels;
            $scope.addUriText = '';
    	    $scope.uriInDict = false;

            $scope.updateVal = function() {
                if($scope.addUriText.match("^http://")) {
                    $scope.val = $scope.addUriText;
                }
            };

            $scope.updateUriLabelDict = function(k,v) {
                $scope.uriLabels[k] = v;
            };
            $scope.$watch("addUriText", function(newValue, oldValue){
    	    	$scope.uriInDict = (($scope.dataquery!='') && ($scope.addUriText in $scope.uriLabels));
    	    });
        }
    };
});

app.directive('languagesListInput', function(RecordModel, context) {
    return {
        restrict: 'E',
        replace: true,
        transclude: true,
        scope: {
        	obj:"=",
        },
        templateUrl: function(tElement, tAttrs) {
            return context.urls.base_static+'p4l/templates/languagesListInput.html';  
        },
        link: function($scope, $element, $attrs) {
            // Get list from context languages_list
            $scope.list = context.languages_list;
        }
    };
});

app.controller("RecordCtrl", function($translate, $scope, $location, RecordModel, context, $log, p4lConfig, $window){
    
    $scope.record = RecordModel.record;
    $scope.uriLabels = RecordModel.uriLabels;
    
    $scope.saving = false;
    $scope.contentLoaded = false;
    $scope.recordDirty = false;
    
    $translate([
        "An error occured. Somes datas may be incorrect or incomplete.",
        "This page is asking you to confirm that you want to leave - data you have entered may not be saved."
    ]).then(function(translations) {
        $scope.translations = translations;
    });
    
    $scope.$on('$includeContentLoaded', function(event) { event.currentScope.contentLoaded = true; });
        
    $scope.submitRecord = function() {
        $scope.saving = true;
        $scope.record.$save({ recordId: context.record_id })
            .then(
                function(response) {
                    if(context.is_create_view) {
                        $location.path(decodeURI(context.urls.record_edit.replace(":recordId", context.record_id))).search({previous:$scope.getPreviousUrl()}).replace();
                    }
                },
                function(reason){
                    alert($scope.translations["An error occured. Somes datas may be incorrect or incomplete."]);
                }
            )
            .finally(function() {
                $scope.saving = false;
                $scope.recordDirty = false;
            });
    }
    
    $scope.getPreviousUrl = function() {
        return context.urls.previous || context.urls.home;
    }

    $scope.$watch(
        function(s) {
            return context.record;
        },
        function(newValue, oldValue, s) {
            if(s.contentLoaded) {
                s.recordDirty = true;
            }
        },
        true
    );
    
    $window.onbeforeunload = function() {
        if($scope.recordDirty) {
            var msg = $scope.translations["This page is asking you to confirm that you want to leave - data you have entered may not be saved."]; 
            return msg;
        }
    }
    
});

app.config(['$routeProvider', function($routeProvider) {
//    $routeProvider.when('/', {controller: 'RecordCtrl', templateUrl: 'partials/record.html'});
//    $routeProvider.otherwise({redirectTo: '/'});
  }]);

