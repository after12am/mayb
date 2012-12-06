(function($) {

 // js/app/app.js

var app = {};

$(function() {
    
    app.AppView = new AppView();
});
// js/app/utils.js

var toQuery = function(object) {
    
    var arr = new Array();
    
    for (var name in object) {
        arr.push(name + '=' + object[name]);
    }
    
    return arr.join('&');
}
// js/app/view/AppView.js

var AppView = Backbone.View.extend({
    
    el: 'body',
    
    offset: 0,
    
    n: 20,
    
    processing: false,
    
    initialize: function() {
        
        _.bindAll(this, 'addPins', 'addPin', 'addRecommendations', 'addRecommendation', 'requestRecos', 'showRecos', 'hideRecos', 'autopage');
        
        this.events = {
            'click .expose div.pin': this.requestRecos,
            'click div.tab': this.showRecos,
            'click div.recommendations': this.hideRecos,
            'click div.recommendations img': this.open
        };
        
        var data = {
            offset: this.offset,
            n: this.n
        };
        
        this.processing = true;
        
        $.get('cgi-bin/expose.py', toQuery(data), $.proxy(function(data) {
            
            // initialize masonry
            $(this.el).find('#container').masonry({
                itemSelector : '.pin',
                columnWidth : 10
            });
            
            this.addPins(data);
            // set event after getting first data set.
            $(window).scroll(this.autopage);
            
            var that = this;
            // adjust layout
            setInterval(function() {
                $(that.el).find('#container').masonry( 'reload');
            }, 1000);
            
            this.processing = false;
            
        }, this));
    },
    
    addPins: function(data) {
        
        // set next offset
        this.offset += this.n;
        
        for (var i in data) {
            this.addPin(data[i]);
        }
    },
    
    addPin: function(data) {
        var item = new ItemView();
        item.data = data;
        item.render();
    },
    
    addRecommendations: function(data) {
        
        $(this.el).find('div.recommendations .recommended').remove();
        
        for (var i in data) {
            this.addRecommendation(data[i]);
        }
    },
    
    addRecommendation: function(data) {
        var item = new RecommendedItemView();
        item.data = data;
        item.render();
    },
    
    requestRecos: function(e) {
        
        var pin_id = $(e.currentTarget).attr('pin-id');
        // console.log(pin_id);
        
        this.showRecos();
        
        $.get('cgi-bin/recommendations.py', 'pin_id=' + pin_id, this.addRecommendations);
    },
    
    showRecos: function() {
        
        $(this.el).find('div.recommendations').removeClass('rotate180').addClass('rotate0');
        $(this.el).find('div.tab').removeClass('rotate0').addClass('rotate180');
    },
    
    hideRecos: function() {
        
        $(this.el).find('div.recommendations').removeClass('rotate0').addClass('rotate180');
        $(this.el).find('div.tab').removeClass('rotate180').addClass('rotate0');
    },
    
    autopage: function() {
        
        if (this.processing) return;
        
        var ch = $('header').height() + $('#container').height();
        var wh = $(window).height();
        var top = $(window).scrollTop();
        
        if (top > (ch - wh) - 100) {
            
            var data = {
                offset: this.offset,
                n: this.n
            };
            
            this.processing = true;
            
            $.get('cgi-bin/expose.py', toQuery(data), $.proxy(function(data) {
                
                this.addPins(data);
                this.processing = false;
                
            }, this));
        }
    },
    
    open: function(e) {
        
        console.log()
        
        window.open($(e.currentTarget).parent().attr('href'));
        return false;
    }
});
// js/app/view/ItemView.js

var ItemView = Backbone.View.extend({
    
    el: '.expose',
    
    template: _.template($('#item-template').html()),
    
    data: {},
    
    initialize: function() {
        
        _.bindAll(this, 'render');
    },
    
    render: function() {
        
        var data = {
            'pin_id': this.data.pin_id,
            'uri': this.data.uri
        }
        
        $(this.el).append(this.template(data));
        
        return this;
    }
});
// js/app/view/RecommendedItemView.js

var RecommendedItemView = Backbone.View.extend({
    
    el: '.recommendations',
    
    template: _.template($('#recommended-item-template').html()),
    
    data: {},
    
    initialize: function() {
        
        _.bindAll(this, 'render');
    },
    
    render: function() {
        
        var data = {
            'pin_id': this.data.pin_id,
            'uri': this.data.uri
        }
        
        $(this.el).append(this.template(data));
        
        return this;
    }
}); 

})(jQuery);