var Slider = function ($el, callback, max) {
    
    // save the element
    this.$el = $el
    this.callback = callback   

    // update function
    this.update = function (percentage) {
        // set the percentage
        this.$el.val((percentage/100) * this.max)
    }

    // access the maximum function
    this.setMax = function (max) {
        // set the maximum if requested
        if (max != undefined) {
            // set the maximum
            this.max = max
            
            // set in tag
            this.$el.prop('max', max)
        }
        // return maximum
        return this.max
    }
    
    // if we didn't get a maximum get it from the element
    if (max == undefined)
        max = $el.prop('max')

    // set maximum
    this.setMax(max)

    // set the callback
    this.$el.on("change", function () {
        // get percentage
        var percentage = 100 * this.$el.val() / this.max

        // call the callback
        callback( percentage)
    }.bind(this))

    // return self
    return this;
}
