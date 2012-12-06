
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