## create utils for the app


def populate_form(links, form):

    ## adding the links and titles
    for i,l in enumerate(links):

        if i == 0:
            form.link1_title.data = l.link_title;
            form.link1.data = l.link_url;

        if i == 1:
            form.link2_title.data = l.link_title;
            form.link2.data = l.link_url;

        if i == 2:
            form.link3_title.data = l.link_title;
            form.link3.data = l.link_url;
