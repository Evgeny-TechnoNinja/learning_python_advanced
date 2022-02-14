def head(element_head) -> str:
    """
    Serves as head element
    :param element_head: Elements to be inserted into the head, styles css
    :return: string with html element head
    """
    return f"""
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" 
            integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
        {element_head}
    </head>
    """


def navigation(link_name_a="link_a", link_a_path="#",
               link_name_b="link_b", link_b_path="#",
               link_name_c="link_c", link_c_path="#",
               link_name_d="link_d", link_d_path="#") -> dict:
    """
    Create site navigation. Site menu. Four-item menu
    :param link_name_a: link name
    :param link_a_path: the path to the resource that matches the link name
    :param link_name_b: link name
    :param link_b_path: the path to the resource that matches the link name
    :param link_name_c: link name
    :param link_c_path: the path to the resource that matches the link name
    :param link_name_d: link name
    :param link_d_path: the path to the resource that matches the link name
    :return: Dictionary with navigation styles and navigation
    """
    nav = f"""
    <nav class="navbar navbar-expand-lg fixed-top">
        <ul class="navbar-nav mr-4">
             <li class="nav-item">
                <a class="nav-link" href="{link_a_path}">&#x25BA; {link_name_a}</a> 
             </li>
             <li class="nav-item">
                <a class="nav-link" href="{link_b_path}">&#x25BA; {link_name_b}</a> 
             </li>
             <li class="nav-item">
                <a class="nav-link" href="{link_c_path}">&#x25BA; {link_name_c}</a> 
             </li>
              <li class="nav-item">
                <a class="nav-link" href="{link_d_path}">&#x25BA; {link_name_d}</a> 
             </li>
        </ul> 
    </nav>
    """
    nav_style = """
        .navbar { background: #002b36; padding: 10px 40px;}
        .nav-link , .navbar-brand { color: #fdf6e3; cursor: pointer; font-family: monospace;}
        .nav-link:hover{ color: #cb4b16;}
    """
    return {"nav": nav, "nav_style": nav_style}


def section_style():
    """
    Section Styles CSS
    :return: style selector
    """
    return """
        .section {
            background: -webkit-linear-gradient(180deg, rgb(210, 225, 222) 96%, rgb(0, 43, 54) 52%);
            background: -moz-linear-gradient(180deg, rgb(210, 225, 222) 96%, rgb(0, 43, 54) 52%);
            background: linear-gradient(180deg, rgb(210, 225, 222) 96%, rgb(0, 43, 54) 52%);
            height: 100vh;
        }
    """


def description_style():
    """
    Styles for paragraphs and headings
    :return: two selectors
    """
    return """
        .description {
            margin: 200px auto;
            font-family: monospace;
            text-align: center;
        }
        .description h1, h2, h3{
            color:#d33682;
        }
    """


def wrap_style():
    """
    Wrapper for positioning
    :return: selector
    """
    return """
    .wrap {
        display: flex;
	    height: 350px;
    }
    """ # noqa


def pre_style():
    """
    Styles block code
    :return: selector
    """
    return """
        pre {
            padding-left: 5px;
            max-width: 900px;
            max-height: 350px;
            text-align: left;
            color: #00ff0a;
            background: black;
        }
    """


def form_style():
    """
    Style for form
    :return: selector
    """
    return """
        form {
            margin-top: 30px;
        }
    """


def big_txt():
    """
    Styles for cool text
    :return: selector
    """
    return """
        .big-txt {
            font-size: 20px;
        }
    
    """