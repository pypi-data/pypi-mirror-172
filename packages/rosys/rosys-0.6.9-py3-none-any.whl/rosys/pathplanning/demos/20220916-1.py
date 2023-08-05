from rosys.geometry import Point, Pose
from rosys.pathplanning.area import Area
from rosys.pathplanning.obstacle import Obstacle
from rosys.pathplanning.planner_process import PlannerSearchCommand

robot_outline = [(-0.22, -0.36), (1.07, -0.36), (1.17, 0), (1.07, 0.36), (-0.22, 0.36)]

cmd = PlannerSearchCommand(
    deadline=1663319516.2077515,
    areas=[
        Area(
            id='08d833cb-1f99-41aa-b6c7-fc0e8708a503', type='sand', color='SandyBrown',
            outline=[Point(x=1.0590359129975533, y=4.244390327913762),
                     Point(x=1.0192112908916058, y=5.304530017412585),
                     Point(x=3.501992817804549, y=5.669401956748319),
                     Point(x=5.17858898590781, y=7.230093995319592),
                     Point(x=8.94957905072724, y=7.15569656984405),
                     Point(x=8.38527067601789, y=16.8738254181317),
                     Point(x=2.1972965612353885, y=19.771454986485764),
                     Point(x=3.999888915460003, y=23.027086130169394),
                     Point(x=12.37348912258075, y=21.076070634348476),
                     Point(x=11.1902267381961, y=16.4664623004856),
                     Point(x=15.669612048125, y=14.7992335540578),
                     Point(x=15.421032122978, y=6.81613943873455),
                     Point(x=15.397656629262237, y=-0.9423851148888711),
                     Point(x=8.790230498500804, y=-1.0571009685429216),
                     Point(x=3.047683694391778, y=-2.196583645938693),
                     Point(x=3.1073318516475457, y=-0.732022040537003),
                     Point(x=1.4883934239195065, y=-1.0112902149551632),
                     Point(x=1.1301893501312854, y=-0.6391648260724812),
                     Point(x=0.7027086287015161, y=-0.386541211458467)]),
        Area(id='37ae7616-47d0-41fe-82e7-2c888f91eb9e', type=None, color='green', outline=[]),
        Area(
            id='d36c22e0-63fb-40d8-8456-a8b3d24c3d01', type=None, color='green',
            outline=[Point(x=2.80797229072323, y=-0.8764971670364472),
                     Point(x=1.3332961547721252, y=-1.189707759237689),
                     Point(x=1.0117832718954882, y=-0.8264371843594254),
                     Point(x=0.5080050112589248, y=-0.9754465040484206),
                     Point(x=0.5096212015855641, y=-2.072928650699689),
                     Point(x=-0.8072751698417473, y=-2.0595028772922337),
                     Point(x=-0.973041750299013, y=-0.7662223013940208),
                     Point(x=-1.9805655443972054, y=-0.611159965693066),
                     Point(x=-2.868385715409263, y=3.7445767265126957),
                     Point(x=-0.31127645714462227, y=4.127711442625058),
                     Point(x=0.3056607484889565, y=3.675935769785664),
                     Point(x=0.2633899547759206, y=1.462530965434138),
                     Point(x=0.8227877715339622, y=1.5525455689429561),
                     Point(x=0.8091683622973789, y=3.8842261395910223),
                     Point(x=0.910301043888975, y=5.695847113101454),
                     Point(x=1.4938752585504136, y=5.847776506382744),
                     Point(x=1.7395989750547711, y=7.425311662384807),
                     Point(x=8.652920143943527, y=7.371499247570442),
                     Point(x=7.93263728100243, y=16.80572682550201),
                     Point(x=1.9571882282210222, y=19.634416034284172),
                     Point(x=4.04113064630966, y=23.426845779569433),
                     Point(x=12.848563494379663, y=21.29868712962107),
                     Point(x=11.44648745644847, y=16.596025437789887),
                     Point(x=16.020973164980198, y=15.003361363350756),
                     Point(x=15.555691521508031, y=-1.2355241157925636),
                     Point(x=8.847292236083893, y=-1.297345468319342),
                     Point(x=2.8523427352810966, y=-2.343134995446132)])],
    obstacles=[
        Obstacle(
            id='54cc30bb-d46b-4d13-aacb-0dca31ee5982',
            outline=[Point(x=10.223293537911058, y=4.584916180325653),
                     Point(x=9.95269548783796, y=4.855514230398751),
                     Point(x=9.57001205547287, y=4.855514230398751),
                     Point(x=9.299414005399772, y=4.584916180325653),
                     Point(x=9.299414005399772, y=4.202232747960563),
                     Point(x=9.57001205547287, y=3.931634697887465),
                     Point(x=9.95269548783796, y=3.9316346978874646),
                     Point(x=10.223293537911058, y=4.202232747960563)]),
        Obstacle(
            id='20507bb1-91fb-4a52-908d-2ef0c8b91e47',
            outline=[Point(x=9.370696742117035, y=4.559763096843733),
                     Point(x=9.100098692043938, y=4.8303611469168315),
                     Point(x=8.717415259678846, y=4.8303611469168315),
                     Point(x=8.446817209605749, y=4.559763096843733),
                     Point(x=8.446817209605749, y=4.177079664478644),
                     Point(x=8.717415259678846, y=3.9064816144055454),
                     Point(x=9.100098692043938, y=3.906481614405545),
                     Point(x=9.370696742117035, y=4.177079664478644)]),
        Obstacle(
            id='f342d0f6-9969-4211-94e5-adc9cc719a07',
            outline=[Point(x=8.582913870987802, y=4.61306767481214),
                     Point(x=8.312315820914705, y=4.883665724885239),
                     Point(x=7.9296323885496145, y=4.883665724885239),
                     Point(x=7.659034338476516, y=4.61306767481214),
                     Point(x=7.659034338476516, y=4.230384242447051),
                     Point(x=7.9296323885496145, y=3.9597861923739526),
                     Point(x=8.312315820914705, y=3.959786192373952),
                     Point(x=8.582913870987802, y=4.230384242447051)]),
        Obstacle(
            id='5810ca18-3242-4a15-9076-659dd7e1494f',
            outline=[Point(x=7.718790795847545, y=4.728740482678204),
                     Point(x=7.448192745774446, y=4.9993385327513025),
                     Point(x=7.065509313409357, y=4.9993385327513025),
                     Point(x=6.7949112633362585, y=4.728740482678204),
                     Point(x=6.7949112633362585, y=4.346057050313115),
                     Point(x=7.065509313409357, y=4.075459000240016),
                     Point(x=7.448192745774446, y=4.075459000240016),
                     Point(x=7.718790795847545, y=4.346057050313115)]),
        Obstacle(
            id='82da6786-f040-419a-9885-c530b0cb8975',
            outline=[Point(x=7.1466477324269775, y=4.905989455612645),
                     Point(x=6.876049682353879, y=5.1765875056857436),
                     Point(x=6.49336624998879, y=5.1765875056857436),
                     Point(x=6.222768199915691, y=4.905989455612645),
                     Point(x=6.222768199915691, y=4.523306023247556),
                     Point(x=6.49336624998879, y=4.2527079731744575),
                     Point(x=6.876049682353879, y=4.2527079731744575),
                     Point(x=7.1466477324269775, y=4.523306023247556)]),
        Obstacle(
            id='92df51d3-6228-4354-8fd1-4b326a9b56b3',
            outline=[Point(x=6.514169658915937, y=4.734007896442819),
                     Point(x=6.243571608842839, y=5.004605946515917),
                     Point(x=5.860888176477749, y=5.004605946515917),
                     Point(x=5.590290126404651, y=4.734007896442819),
                     Point(x=5.590290126404651, y=4.351324464077729),
                     Point(x=5.860888176477749, y=4.080726414004631),
                     Point(x=6.243571608842839, y=4.080726414004631),
                     Point(x=6.514169658915937, y=4.351324464077729)]),
        Obstacle(
            id='bdad1517-9301-4a39-80db-d36216b1d966',
            outline=[Point(x=6.123980438627834, y=4.305649877640608),
                     Point(x=5.853382388554736, y=4.576247927713706),
                     Point(x=5.470698956189646, y=4.576247927713706),
                     Point(x=5.200100906116548, y=4.305649877640608),
                     Point(x=5.200100906116548, y=3.9229664452755184),
                     Point(x=5.470698956189646, y=3.65236839520242),
                     Point(x=5.853382388554736, y=3.6523683952024197),
                     Point(x=6.123980438627834, y=3.922966445275518)]),
        Obstacle(
            id='9260cec7-cf8e-45f6-9299-2d88d18d194f',
            outline=[Point(x=6.0584708734537775, y=3.759715655519662),
                     Point(x=5.787872823380679, y=4.030313705592761),
                     Point(x=5.40518939101559, y=4.030313705592761),
                     Point(x=5.1345913409424915, y=3.759715655519662),
                     Point(x=5.1345913409424915, y=3.3770322231545724),
                     Point(x=5.40518939101559, y=3.1064341730814737),
                     Point(x=5.787872823380679, y=3.1064341730814737),
                     Point(x=6.0584708734537775, y=3.377032223154572)]),
        Obstacle(
            id='58bfe6bd-81e9-443d-a419-f67b6bc4be73',
            outline=[Point(x=6.0539271876460905, y=2.9269850687060046),
                     Point(x=5.783329137572992, y=3.1975831187791033),
                     Point(x=5.400645705207903, y=3.1975831187791033),
                     Point(x=5.130047655134804, y=2.9269850687060046),
                     Point(x=5.130047655134804, y=2.544301636340915),
                     Point(x=5.400645705207903, y=2.2737035862678168),
                     Point(x=5.783329137572992, y=2.2737035862678163),
                     Point(x=6.0539271876460905, y=2.5443016363409146)]),
        Obstacle(
            id='89fe00b1-33b1-436f-ace9-99ca6ded085b',
            outline=[Point(x=5.9888621971334794, y=2.3862796094372016),
                     Point(x=5.718264147060381, y=2.6568776595103003),
                     Point(x=5.335580714695292, y=2.6568776595103003),
                     Point(x=5.064982664622193, y=2.3862796094372016),
                     Point(x=5.064982664622193, y=2.003596177072112),
                     Point(x=5.335580714695292, y=1.7329981269990136),
                     Point(x=5.718264147060381, y=1.7329981269990136),
                     Point(x=5.9888621971334794, y=2.0035961770721116)]),
        Obstacle(
            id='140ff896-7a25-47be-ae7b-fe1cf43c5138',
            outline=[Point(x=10.351975204872746, y=3.7777979871605725),
                     Point(x=10.081377154799648, y=4.048396037233671),
                     Point(x=9.698693722434557, y=4.048396037233671),
                     Point(x=9.42809567236146, y=3.7777979871605725),
                     Point(x=9.42809567236146, y=3.395114554795483),
                     Point(x=9.698693722434557, y=3.1245165047223846),
                     Point(x=10.081377154799648, y=3.124516504722384),
                     Point(x=10.351975204872746, y=3.3951145547954824)]),
        Obstacle(
            id='8b7a9f6d-2323-4cdd-b9f4-1623dc3aa444',
            outline=[Point(x=10.286277714649838, y=3.2323743742269135),
                     Point(x=10.01567966457674, y=3.502972424300012),
                     Point(x=9.63299623221165, y=3.502972424300012),
                     Point(x=9.362398182138552, y=3.2323743742269135),
                     Point(x=9.362398182138552, y=2.849690941861824),
                     Point(x=9.63299623221165, y=2.5790928917887257),
                     Point(x=10.01567966457674, y=2.5790928917887253),
                     Point(x=10.286277714649838, y=2.8496909418618235)]),
        Obstacle(
            id='02082a83-3c96-47c2-8ef4-5393fffc1ef9',
            outline=[Point(x=10.325793409284863, y=2.685617908239653),
                     Point(x=10.055195359211766, y=2.9562159583127516),
                     Point(x=9.672511926846674, y=2.9562159583127516),
                     Point(x=9.401913876773577, y=2.685617908239653),
                     Point(x=9.401913876773577, y=2.3029344758745633),
                     Point(x=9.672511926846674, y=2.032336425801465),
                     Point(x=10.055195359211766, y=2.0323364258014647),
                     Point(x=10.325793409284863, y=2.302934475874563)]),
        Obstacle(
            id='352d41e5-d1f9-4207-aaff-439ea6d15c74',
            outline=[Point(x=9.441323640321542, y=3.64690088870541),
                     Point(x=8.900127540175346, y=4.1880969888516075),
                     Point(x=8.134760675445166, y=4.1880969888516075),
                     Point(x=7.593564575298969, y=3.6469008887054106),
                     Point(x=7.593564575298969, y=2.881534023975231),
                     Point(x=8.134760675445166, y=2.340337923829034),
                     Point(x=8.900127540175346, y=2.340337923829034),
                     Point(x=9.441323640321542, y=2.88153402397523)]),
        Obstacle(
            id='08cb104b-69d6-4a58-99f1-5807547ddb05',
            outline=[Point(x=7.765403899368146, y=4.054457839355827),
                     Point(x=7.224207799221949, y=4.595653939502023),
                     Point(x=6.45884093449177, y=4.595653939502023),
                     Point(x=5.917644834345572, y=4.054457839355827),
                     Point(x=5.917644834345572, y=3.289090974625647),
                     Point(x=6.458840934491769, y=2.7478948744794502),
                     Point(x=7.224207799221949, y=2.7478948744794502),
                     Point(x=7.765403899368145, y=3.2890909746256463)]),
        Obstacle(
            id='222ced43-4a30-47be-ae8c-b81e56d68538',
            outline=[Point(x=7.6003494970557375, y=2.4646774848356343),
                     Point(x=7.05915339690954, y=3.005873584981831),
                     Point(x=6.293786532179361, y=3.005873584981831),
                     Point(x=5.752590432033164, y=2.4646774848356348),
                     Point(x=5.752590432033164, y=1.699310620105455),
                     Point(x=6.29378653217936, y=1.1581145199592582),
                     Point(x=7.05915339690954, y=1.1581145199592582),
                     Point(x=7.600349497055737, y=1.6993106201054542)]),
        Obstacle(
            id='95504d6f-843f-4f7d-8e63-b46dbbec82a6',
            outline=[Point(x=9.26816467254988, y=2.1303517430018597),
                     Point(x=8.726968572403683, y=2.6715478431480566),
                     Point(x=7.961601707673504, y=2.6715478431480566),
                     Point(x=7.420405607527306, y=2.13035174300186),
                     Point(x=7.420405607527306, y=1.3649848782716805),
                     Point(x=7.961601707673503, y=0.8237887781254836),
                     Point(x=8.726968572403683, y=0.8237887781254835),
                     Point(x=9.26816467254988, y=1.3649848782716796)]),
        Obstacle(
            id='63023441-d1d7-4f00-903d-0c79434bff46',
            outline=[Point(x=8.437719663357418, y=0.7561489829803368),
                     Point(x=8.16712161328432, y=1.0267470330534354),
                     Point(x=7.78443818091923, y=1.0267470330534354),
                     Point(x=7.513840130846131, y=0.7561489829803368),
                     Point(x=7.513840130846131, y=0.3734655506152471),
                     Point(x=7.78443818091923, y=0.10286750054214866),
                     Point(x=8.16712161328432, y=0.1028675005421486),
                     Point(x=8.437719663357418, y=0.3734655506152467)]),
        Obstacle(
            id='daad455a-e6f8-47cf-9140-ac090674d35e',
            outline=[Point(x=7.958352963166784, y=0.7917382324576797),
                     Point(x=7.687754913093686, y=1.062336282530778),
                     Point(x=7.305071480728596, y=1.062336282530778),
                     Point(x=7.034473430655498, y=0.7917382324576797),
                     Point(x=7.034473430655498, y=0.40905480009259),
                     Point(x=7.305071480728596, y=0.13845675001949154),
                     Point(x=7.687754913093686, y=0.13845675001949148),
                     Point(x=7.958352963166784, y=0.4090548000925896)]),
        Obstacle(
            id='295283b8-c0c2-4037-8452-7719f7432072',
            outline=[Point(x=6.951473557281621, y=5.489284651217086),
                     Point(x=6.680875507208523, y=5.759882701290184),
                     Point(x=6.298192074843433, y=5.759882701290184),
                     Point(x=6.027594024770335, y=5.489284651217086),
                     Point(x=6.027594024770335, y=5.1066012188519965),
                     Point(x=6.298192074843433, y=4.836003168778898),
                     Point(x=6.680875507208523, y=4.836003168778898),
                     Point(x=6.951473557281621, y=5.1066012188519965)])],
    start=Pose(x=3.385765303231167, y=6.230644699650673, yaw=3.000494384983233, time=1663319496.187386),
    goal=Pose(x=5.251101287617182, y=5.479623558637116, yaw=-1.9198621771937632, time=0))
