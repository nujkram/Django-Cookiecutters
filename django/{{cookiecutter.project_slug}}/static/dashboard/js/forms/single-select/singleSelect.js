/*
 * Requires:
 * - jQuery
 * - bootstrap.js
 * - jQuery.loadTemplate
 * - jQuery.toast
 */
function SingleSelect(props){
    this.p = {
        objState: props.objState,
        baseObjState: props.objState,
        gui: {
            btns: {
                trigger: props.gui.btns.trigger,
            },
            search: props.search,
            forms: {
                select: props.gui.forms.select,
                create: props.gui.forms.create
            },
            con: {
                choices: props.gui.con.choices,
            },
            tpl: {
                choices: props.gui.tpl.choices
            },
            field: props.gui.field,
            modal: props.gui.modal
        },
        urls: {
            list: props.urls.list,
            create: props.urls.create
        }
    };

    this.load = function(s, prop){
        if(prop !== null){
            var p = prop;
        }else{
            var p = this.p;
        }
        var url = p.urls.list;
        if(s.trim().length > 0){
            if(s.indexOf("?") !== -1){
                url = url + "?q=" + s;
            }else {
                url = url + "&s=" + s;
            }
        }

        p.gui.con.choices.html("<div class='preloader'></div>");

        $.get(url)
            .done(function(result){
                p.gui.con.choices.loadTemplate(p.gui.tpl.choices, result);
            })
            .fail(function(e){
                console.log(e);
            });
    };

    this.resetObjState = function(p){
        p.objState = p.baseObjState;
    };

    this.populateChoice =  function(p){
        p.gui.field.val(p.objState.id);
        p.gui.btns.trigger.val(p.objState.name);
    };

    this.selectChoice = function(p, value, name){
        p.objState.id = value;
        p.objState.name = name;
        this.populateChoice(p);
        p.gui.modal.modal('hide');
    };

    this.create = function(formData){
        var p = this.p;
        var that = this;
        var load = this.load;
        var resetObjState = this.resetObjState;
        var populateChoice = this.populateChoice;

        var url = p.urls.create;
        $.post(url, formData)
            .done(function(result){
                $.toast({
                    text: "Success!",
                    position: 'top-right',
                    allowToastClose: true,
                    bgColor: '#00e676',
                    textColor: '#f5f5f5',
                });
                load('', p);
                resetObjState(p);
                populateChoice(p);
            })
            .fail(function(e){
                console.log(e);
            });
    }

}
