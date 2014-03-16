# Game services for Android
from jnius import autoclass, PythonJavaClass, java_method
from android.runnable import run_on_ui_thread
import android
import android.activity
PythonActivity = autoclass('org.renpy.android.PythonActivity')
GameHelper = autoclass('com.google.example.games.basegameutils.GameHelper')
Games = autoclass('com.google.android.gms.games.Games')


class GameHelperListener(PythonJavaClass):
    __javacontext__ = 'app'
    __javainterfaces__ = ['com.google.example.games.basegameutils.GameHelper$GameHelperListener']

    @java_method('()V')
    def onSignInFailed(self):
        print 'signing failed :('

    @java_method('()V')
    def onSignInSucceeded(self):
        print 'signin success :)'

gh_instance = None
gh_instance_listener = None

def _on_activity_result(request, response, data):
    gh_instance.onActivityResult(request, response, data)

@run_on_ui_thread
def setup(app):
    global gh_instance
    global gh_instance_listener


    gh_instance = GameHelper(PythonActivity.mActivity, GameHelper.CLIENT_ALL)
    #gh_instance.enableDebugLog(True)
    gh_instance_listener = GameHelperListener()
    gh_instance.setup(gh_instance_listener)
    gh_instance.onStart(PythonActivity.mActivity)
    android.activity.unbind(on_activity_result=_on_activity_result)
    android.activity.bind(on_activity_result=_on_activity_result)

def unlock(uid):
    if not gh_instance.isSignedIn():
        return
    Games.Achievements.unlock(gh_instance.getApiClient(), uid)

def increment(uid, count):
    if not gh_instance.isSignedIn():
        return
    Games.Achievements.increment(gh_instance.getApiClient(), uid, count)

def leaderboard(uid, score):
    if not gh_instance.isSignedIn():
        return
    Games.Leaderboards.submitScore(gh_instance.getApiClient(), uid, score)

def show_leaderboard(uid):
    if not gh_instance.isSignedIn():
        return
    PythonActivity.mActivity.startActivityForResult(
        Games.Leaderboards.getLeaderboardIntent(
            gh_instance.getApiClient(), uid), 0x6601)

def show_achievements():
    if not gh_instance.isSignedIn():
        return
    PythonActivity.mActivity.startActivityForResult(
        Games.Achievements.getAchievementsIntent(
            gh_instance.getApiClient()), 0x6602)

def on_stop():
    gh_instance.onStop()

def on_start():
    gh_instance.onStart(PythonActivity.mActivity)
