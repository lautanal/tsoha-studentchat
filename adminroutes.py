from app import app
from flask import render_template, request, redirect, flash
import users, areas, topics, messages, admins

# Admin aloitus
@app.route("/admin")
def admin():
    return render_template("adindex.html", login="yes")

# Admin päävalikko
@app.route("/admin/menu")
def ad_menu():
    if admins.admin_id() == 0:
        return render_template("adindex.html", login="yes")
    else:
        return render_template("admenu.html")

# Keskustelualueiden hallinta
@app.route("/admin/areas")
def ad_list_areas():
    if admins.admin_id()== 0:
        return render_template("adindex.html", login="yes")
    else:
        alist = areas.get_areas_all()
        return render_template("adareas.html", areas=alist)

# Viestiketjujen listaus
@app.route("/admin/topics/<int:area_id>")
def ad_list_topics(area_id):
    if admins.admin_id() == 0:
        return render_template("adindex.html", login="yes")
    else:
        area_name = areas.get_areaname(area_id)
        tlist = topics.get_topics_all(area_id)
        return render_template("adtopics.html", area_id=area_id, area_name=area_name, topics=tlist)

# Viestiketjun sulkeminen
@app.route("/admin/locktopic/<int:area_id>/<int:topic_id>")
def ad_lock_topic(area_id, topic_id):
    if admins.admin_id() == 0:
        return render_template("adindex.html", login="yes")
    else:
        topics.lock_topic(topic_id)
        area_name = areas.get_areaname(area_id)
        tlist = topics.get_topics_all(area_id)
        return render_template("adtopics.html", area_id=area_id, area_name=area_name, topics=tlist)

# Viestiketjun avaaminen
@app.route("/admin/opentopic/<int:area_id>/<int:topic_id>")
def ad_open_topic(area_id, topic_id):
    if admins.admin_id() == 0:
        return render_template("adindex.html", login="yes")
    else:
        topics.open_topic(topic_id)
        area_name = areas.get_areaname(area_id)
        tlist = topics.get_topics_all(area_id)
        return render_template("adtopics.html", area_id=area_id, area_name=area_name, topics=tlist)

# Viestien hallinta
@app.route("/admin/messages/<int:topic_id>")
def ad_list_messages(topic_id):
    if admins.admin_id() == 0:
        return render_template("adindex.html", login="yes")
    else:
        area_id = topics.get_area_id(topic_id)
        area_name = areas.get_areaname(area_id)
        topic_name = topics.get_topicname(topic_id)
        list = messages.get_messages(topic_id)
        return render_template("admessages.html", area_id=area_id, area_name=area_name, topic_id=topic_id, topic_name=topic_name, count=len(list), messages=list)

# Uusi keskustelualue
@app.route("/admin/newarea")
def newarea():
    return render_template("newarea.html")

# Uuden keskustelualueen talletus tietokantaan
@app.route("/admin/areasend", methods=["post"])
def areasend():
    if admins.admin_id() == 0:
        return render_template("adindex.html", login="yes")
    else:
        area_name = request.form["areaname"]
        hidden = request.form["hidden"]
        if isBlank(area_name) :
                return render_template("newarea.html",error="Tyhjä kenttä, keskustelualuetta ei aloitettu")
        if areas.sendarea(area_name, hidden):
            return redirect("/admin/areas")
        else:
            return render_template("error.html",message="Viestiketjun talletus ei onnistunut")

# Viestin poisto (näkyvistä)
@app.route("/admin/messagedel/<int:message_id>")
def ad_deletem(message_id):
    if admins.admin_id() == 0:
        return render_template("adindex.html", login="yes")
    else:
        topic_id = messages.get_topic_id(message_id)
        if messages.admin_delete(message_id):
            return redirect("/admin/messages/"+str(topic_id))
        else:
            return render_template("error.html",message="Viestin poisto ei onnistunut")

# Uusi viestiketju
@app.route("/admin/newtopic/<int:area_id>")
def ad_newtopic(area_id):
    if admins.admin_id() == 0:
        return render_template("adindex.html", login="yes")
    else:
        return render_template("adnewtopic.html", area_id=area_id)

# Uuden viestiketjun talletus tietokantaan
@app.route("/admin/topicsend/<int:area_id>", methods=["post"])
def ad_topicsend(area_id):
    if admins.admin_id() == 0:
        return render_template("adindex.html", login="yes")
    else:
        topic_name = request.form["topicname"]
        if isBlank(topic_name) :
                return render_template("adnewtopic.html", area_id=area_id, error="Tyhjä kenttä, viestiketjua ei aloitettu")
        if topics.sendtopic(area_id, topic_name):
            return redirect("/admin/topics/"+str(area_id))
        else:
            return render_template("error.html",message="Viestiketjun talletus ei onnistunut")

# Admin login
@app.route("/adlogin", methods=["get","post"])
def ad_login():
    if request.method == "GET":
        return render_template("adlogin.html", login="yes")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if admins.login(username,password):
            return redirect("/admin/menu")
        else:
            error = "Väärä tunnus tai salasana"
            return render_template("adlogin.html", login="yes", error=error)

# Admin logout
@app.route("/adlogout")
def ad_logout():
    admins.logout()
    return render_template("adlogout.html", login="yes")

# Uusi admin käyttäjä
@app.route("/adregister", methods=["get","post"])
def ad_register():
    if admins.admin_id() == 0:
        return render_template("adindex.html", login="yes")
    else:
        if request.method == "GET":
            return render_template("adregister.html")
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            if admins.register(username,password):
                return redirect("/admin/areas")
            else:
                return render_template("error.html",message="Rekisteröinti ei onnistunut")

# Käyttäjien hallinta
@app.route("/admin/users")
def ad_user_list():
    if admins.admin_id() == 0:
        return render_template("adindex.html", login="yes")
    else:
        admin_name = admins.get_adminname()
        list = users.get_userlist()
        return render_template("adusers.html", admin_name = admin_name, userlist=list)

# Käyttäjän oikeuksien muuttaminen
@app.route("/admin/usermod/<int:user_id>")
def ad_user_mod(user_id):
    if admins.admin_id() == 0:
        return render_template("adindex.html", login="yes")
    else:
        user_data = users.get_userdata(user_id)
        return render_template("adusermod.html", user_id=user_data[0], user_name=user_data[1], user_alias=user_data[2], user_rights=user_data[3])

# Käyttäjäoikeuksien muutoksen talletus tietokantaan
@app.route("/admin/usersave/<int:user_id>", methods=["post"])
def ad_user_save(user_id):
    if admins.admin_id() == 0:
        return render_template("adindex.html", login="yes")
    else:
        user_rights = request.form["privileges"]
        if users.modify(user_id, user_rights):
            return redirect("/admin/users")
        else:
            return render_template("error.html",message="Muutosten talletus ei onnistunut")

def isBlank (myString):
    return not (myString and myString.strip())

