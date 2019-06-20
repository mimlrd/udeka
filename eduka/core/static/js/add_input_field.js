// Add and remove input field

$(document).ready(function() {
	var max_fields      = 3; //maximum input boxes allowed
	var wrapper   		= $("#input_fields_wrap"); //Fields wrapper
	var add_button      = $("#add_field_button"); //Add button ID
  //var remove_button      = $("#remove_field_button"); //Add button ID
  var btn_wrapper   = $("#btn_field");

	// for the update of the post
	var update_add_btn     = $("#update_links_btn"); // Update add button
	var update_wrapper     = $("#update_fields_wrap")

	var x = 1; //initlal text box count
	$(add_button).click(function(e){ //on add input button click
		e.preventDefault();
		if(x < max_fields){ //max input box allowed
			x++; //text box increment
			//$(wrapper).append('<div><input class="input" id="link1_title" name="link1_title" placeholder="Titre du lien" type="text" value=""><a href="#" class="remove_field">Remove</a></div>'); //add input box
      $(wrapper).append(
        `
				<figure class="notification">
						<a class="button is-text" id='remove_field_button'>
							<span class="icon">
								<i class="far fa-trash-alt"></i>
							</span>
							<span>Retirer</span>
						</a>
						<hr class="hr-dotted">

            <label class="label" for="link1_title">ajouter un title pour le lien:</label>
            <div class="control has-icons-left has-icons-right">
              <input class="input" id="link1_title" name="link1_title" placeholder="Titre du lien" type="text" value="">
              <span class="icon is-small is-left">
                <i class="fas fa-heading"></i>
              </span>
            </div>
            <p class="help is-success">Donner un titre pour reconnaitre le lien facilement</p>

          <div class="field">
            <label class="label" for="link1">ajouter un lien:</label>
            <div class="control has-icons-left has-icons-right">
              <input class="input" id="link1" name="link1" placeholder="Le lien" type="text" value="">
              <span class="icon is-small is-left">
                <i class="fas fa-link"></i>
              </span>
            </div>
            <p class="help is-success">Donner un titre pour reconnaitre le lien facilement</p>
					</figure>
        `
      );
		}

	});

	$(wrapper).on("click","#remove_field_button", function(e){ //user click on remove text
		e.preventDefault();
    $(this).parent('figure').remove();
    x--;
	})


	//**************************** UPDATE PAGE ***************************

	$(update_add_btn).click(function(e){
		// here will add the link fields
		e.preventDefault()
		$(update_wrapper).append(

			`
			<figure class="notification">
					<a class="button is-text" id='remove_field_button'>
						<span class="icon">
							<i class="far fa-trash-alt"></i>
						</span>
						<span>Retirer</span>
					</a>
					<hr class="hr-dotted">

					<label class="label" for="link1_title">ajouter un title pour le lien:</label>
					<div class="control has-icons-left has-icons-right">
						<input class="input" id="link1_title" name="link1_title" placeholder="Titre du lien" type="text" value="">
						<span class="icon is-small is-left">
							<i class="fas fa-heading"></i>
						</span>
					</div>
					<p class="help is-success">Donner un titre pour reconnaitre le lien facilement</p>

				<div class="field">
					<label class="label" for="link1">ajouter un lien:</label>
					<div class="control has-icons-left has-icons-right">
						<input class="input" id="link1" name="link1" placeholder="Le lien" type="text" value="">
						<span class="icon is-small is-left">
							<i class="fas fa-link"></i>
						</span>
					</div>
					<p class="help is-success">Donner un titre pour reconnaitre le lien facilement</p>
				</figure>
			`

		);
	})
});
