import {useCallback, useEffect, useState} from 'react';
import {Linking, Pressable, StyleSheet, Text, TextInput, View} from 'react-native';
import NetInfo, {useNetInfo} from '@react-native-community/netinfo';
import {NavigationContainer, useNavigation} from '@react-navigation/native';
import {createBottomTabNavigator} from '@react-navigation/bottom-tabs';
import {createNativeStackNavigator, type NativeStackScreenProps} from '@react-navigation/native-stack';
import {SafeAreaProvider} from 'react-native-safe-area-context';
import {StatusBar} from 'expo-status-bar';
import {Ionicons} from '@expo/vector-icons';
import {api} from './src/api';
import {bundledMembers} from './src/bundledMembers';
import {APP_VERSION, GROUP_CODE, MAX_QUESTION_LENGTH} from './src/config';
import {Card, Eyebrow, Muted, Page, PrimaryButton, SectionTitle, StatusPill, Title} from './src/components';
import {storage} from './src/storage';
import {colors} from './src/theme';
import {localAsk} from './src/localSearch';
import type {AskResult, DirectoryMember, Member, RootStackParamList} from './src/types';

type Tabs = {Home: undefined; Ask: undefined; Directory: undefined; About: undefined};
const Tab = createBottomTabNavigator<Tabs>();
const Stack = createNativeStackNavigator<RootStackParamList>();

function HomeScreen() {
  const net = useNetInfo();
  const navigation = useNavigation<any>();
  return <Page>
    <View style={styles.heroLogoWrap}>
      <View style={styles.heroGlowOuter}/>
      <View style={styles.heroGlowInner}/>
      <View style={styles.heroMark}><Text style={styles.heroMarkText}>G05</Text></View>
    </View>
    <Eyebrow>Team intelligence, in your pocket</Eyebrow>
    <Title>Meet the people behind AgriSoko.</Title>
    <Muted>Ask by name, role, skill, or feature and get a concise profile grounded only in approved team evidence.</Muted>
    <StatusPill online={net.isConnected !== false}/>
    <PrimaryButton label="Ask the team" onPress={() => navigation.navigate('Ask')}/>
    <Card><SectionTitle>Built for clarity</SectionTitle><Muted>Designed for lecturers, evaluators, stakeholders, and visitors who need to understand team ownership quickly—even when connectivity is limited.</Muted></Card>
    <View style={styles.factRow}><View><Eyebrow>Group</Eyebrow><Text style={styles.fact}>{GROUP_CODE}</Text></View><View><Eyebrow>Version</Eyebrow><Text style={styles.fact}>{APP_VERSION}</Text></View></View>
  </Page>;
}

function AskScreen() {
  const navigation = useNavigation<any>();
  const net = useNetInfo();
  const [question, setQuestion] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [cachedResultAvailable, setCachedResultAvailable] = useState<AskResult | null>(null);

  useEffect(() => {
    storage.getResult().then(setCachedResultAvailable).catch(() => undefined);
  }, []);

  const submit = async () => {
    const cleaned = question.trim();
    if (!cleaned) return setError('Enter a question before continuing.');
    if (cleaned.length > MAX_QUESTION_LENGTH) return setError(`Keep your question under ${MAX_QUESTION_LENGTH} characters.`);
    setError(''); setLoading(true);
    try {
      let result: AskResult;
      const state = await NetInfo.fetch();
      if (state.isConnected) {
        try {
          result = await api.ask(cleaned);
          if (result.match) await storage.setProfile(result.match);
        } catch {
          result = localAsk(cleaned, bundledMembers, 'The online request failed, so this result uses information built into the app.');
        }
      } else {
        result = localAsk(cleaned, bundledMembers, 'The device is offline, so this result uses information built into the app.');
      }
      if (result.match) await storage.setProfile(result.match);
      await storage.setResult(result);
      setCachedResultAvailable(result);
      navigation.navigate('Result', {result});
    } catch (caught) {
      const previous = await storage.getResult();
      setCachedResultAvailable(previous);
      setError(caught instanceof Error ? `${caught.message}${previous ? ' (Your previous search result was safely preserved).' : ''}` : 'The service is unavailable. Please retry.');
    } finally { setLoading(false); }
  };

  return <Page><Eyebrow>Ask the team</Eyebrow><Title>What would you like to know?</Title><Muted>Try a person’s name, an alias, a role, a skill, or a feature they built.</Muted><StatusPill online={net.isConnected !== false}/>
    <Card><Text style={styles.label}>Your question</Text><TextInput accessibilityLabel="Question" multiline value={question} onChangeText={value => {setQuestion(value); setError('');}} maxLength={MAX_QUESTION_LENGTH + 1} placeholder="Who built offline mode?" placeholderTextColor="#7E8881" style={styles.input}/><Text style={styles.counter}>{question.length}/{MAX_QUESTION_LENGTH}</Text>{error ? <Text accessibilityRole="alert" style={styles.error}>{error}</Text> : null}<PrimaryButton label="Find a team member" onPress={submit} loading={loading}/>{cachedResultAvailable ? <View style={{marginTop: 10}}><PrimaryButton label="View Last Saved Result" onPress={() => navigation.navigate('Result', {result: cachedResultAvailable})}/></View> : null}</Card>
    <Card><SectionTitle>Good questions</SectionTitle><Muted>“Who works with React Native?”{`\n`}“Tell me about [member name].”{`\n`}“Who built the search API?”</Muted></Card>
  </Page>;
}

function DirectoryScreen() {
  const navigation = useNavigation<any>(); const net = useNetInfo();
  const [members, setMembers] = useState<DirectoryMember[]>(bundledMembers); const [loading, setLoading] = useState(false); const [error, setError] = useState('');
  const load = useCallback(async () => { setLoading(true); setError(''); try { const live = await api.members(); setMembers(live.length ? live : bundledMembers); if (live.length) await storage.setDirectory(live); } catch { setMembers(bundledMembers); setError('The live API is unavailable. Showing the complete directory built into the app.'); } finally {setLoading(false);} }, []);
  useEffect(() => {void load();}, [load]);
  return <Page><Eyebrow>Member directory</Eyebrow><Title>The team, clearly mapped.</Title><StatusPill online={net.isConnected !== false}/>{error ? <Text style={styles.notice}>{error}</Text> : null}{loading ? <Muted>Loading approved members…</Muted> : members.length === 0 ? <Card><SectionTitle>No approved members yet</SectionTitle><Muted>Add reviewed records to ai-api/data/members.json, then refresh.</Muted><PrimaryButton label="Retry" onPress={load}/></Card> : members.map(member => <Pressable accessibilityRole="button" key={member.id} onPress={() => navigation.navigate('Profile', {memberId: member.id})}><Card><Eyebrow>{member.role}</Eyebrow><SectionTitle>{member.fullName}</SectionTitle><Muted>{member.skills.join(' • ') || 'No skills recorded'}</Muted><Text style={styles.link}>View profile →</Text></Card></Pressable>)}</Page>;
}

function AboutScreen() {
  const [model, setModel] = useState<Record<string, unknown> | null>(null);
  useEffect(() => {api.modelInfo().then(setModel).catch(() => undefined);}, []);
  return <Page><Eyebrow>About & evidence</Eyebrow><Title>Transparent by design.</Title><Card><SectionTitle>How matching works</SectionTitle><Muted>Approved profile fields are indexed with TF-IDF using word unigrams and bigrams. Cosine similarity ranks members, and results below the 0.45 safety threshold are rejected. Exact names and aliases receive a documented deterministic match.</Muted></Card><Card><SectionTitle>Model information</SectionTitle><Info label="Version" value={String(model?.modelVersion ?? 'Unavailable offline')}/><Info label="Dataset fingerprint" value={String(model?.datasetFingerprint ?? 'Unavailable offline')}/><Info label="Build commit" value={String(model?.buildCommit ?? 'Unavailable offline')}/></Card><Card><SectionTitle>Privacy & limitations</SectionTitle><Muted>The app answers only from version-controlled, member-approved records. It does not generate biographies or infer missing facts. A no-match is safer than a guess.</Muted></Card></Page>;
}

function ResultScreen({route, navigation}: NativeStackScreenProps<RootStackParamList, 'Result'>) {
  const {result} = route.params;
  return <Page><Eyebrow>{result.source}</Eyebrow><Title>{result.match ? result.match.fullName : 'No confident match'}</Title><Card><SectionTitle>{result.match ? result.match.role : 'Try another question'}</SectionTitle><Muted>{result.introduction ?? result.reason}</Muted>{result.match ? <><Text style={styles.confidence}>{Math.round(result.confidence * 100)}% confidence</Text><Text style={styles.body}><Text style={styles.bold}>Why this result: </Text>{result.reason}</Text><PrimaryButton label="Open complete profile" onPress={() => navigation.navigate('Profile', {memberId: result.match!.id, fallback: result.match!})}/></> : <PrimaryButton label="Ask differently" onPress={() => navigation.goBack()}/>}</Card>{result.match ? <><Card><SectionTitle>What they did</SectionTitle><Info label="Feature" value={result.match.feature}/><Info label="Contribution" value={result.match.contribution}/><Info label="Problem addressed" value={result.match.problem}/></Card><Card><SectionTitle>Skills & evidence</SectionTitle><Muted>{result.match.skills.join(' • ') || 'No verified evidence recorded.'}</Muted><Info label="Verified outcome" value={result.match.outcomeMetric}/><Muted>{result.evidenceLinks.length ? `${result.evidenceLinks.length} evidence link${result.evidenceLinks.length === 1 ? '' : 's'} available in the complete profile.` : 'No verified evidence recorded.'}</Muted></Card></> : <Card><SectionTitle>Search tips</SectionTitle><Muted>Try a first name, surname, nickname, role, skill, feature, or even a close spelling. Examples: “Tell me about Gueylord” or “Who worked on React?”</Muted></Card>}</Page>;
}

function ProfileScreen({route}: NativeStackScreenProps<RootStackParamList, 'Profile'>) {
  const builtIn = bundledMembers.find(item => item.id === route.params.memberId) ?? null;
  const [member, setMember] = useState<Member | null>(route.params.fallback ?? builtIn); const [error, setError] = useState('');
  useEffect(() => {api.member(route.params.memberId).then(async value => {setMember(value); await storage.setProfile(value);}).catch(async () => {const cached = await storage.getProfile(); if (cached?.id === route.params.memberId) setMember(cached); else if (builtIn) {setMember(builtIn); setError('Live API unavailable — showing the profile built into the app.');} else if (!route.params.fallback) setError('This profile could not be found.');});}, [route.params.memberId, route.params.fallback, builtIn]);
  if (!member) return <Page><Title>Member profile</Title><Card><Muted>{error || 'Loading approved profile…'}</Muted></Card></Page>;
  return <Page><Eyebrow>{member.role}</Eyebrow><Title>{member.fullName}</Title><Muted>{member.introductionDraft || 'No approved introduction recorded.'}</Muted><Card><SectionTitle>Professional value</SectionTitle><Info label="Target user" value={member.targetUser}/><Info label="Problem" value={member.problem}/><Info label="Feature" value={member.feature}/></Card><Card><SectionTitle>Contribution & evidence</SectionTitle><Muted>{member.contribution || 'No verified evidence recorded.'}</Muted><Info label="Outcome" value={member.outcomeMetric || 'No verified evidence recorded.'}/><Info label="Tester feedback" value={member.testerFeedback || 'No verified evidence recorded.'}/>{member.evidenceLinks.length ? member.evidenceLinks.map(link => <Pressable key={link} onPress={() => Linking.openURL(link).catch(() => setError('Could not open this link.'))}><Text style={styles.link}>{link}</Text></Pressable>) : <Muted>No verified evidence recorded.</Muted>}{error ? <Text style={styles.error}>{error}</Text> : null}</Card><Card><SectionTitle>Skills</SectionTitle><Muted>{member.skills.join(' • ') || 'No verified evidence recorded.'}</Muted></Card></Page>;
}

function Info({label, value}: {label: string; value: string}) {return <View style={styles.info}><Text style={styles.label}>{label}</Text><Text selectable style={styles.body}>{value || 'No verified evidence recorded.'}</Text></View>;}
const tabIcons: Record<keyof Tabs, {active: keyof typeof Ionicons.glyphMap; inactive: keyof typeof Ionicons.glyphMap}> = {
  Home: {active: 'home', inactive: 'home-outline'},
  Ask: {active: 'sparkles', inactive: 'sparkles-outline'},
  Directory: {active: 'people', inactive: 'people-outline'},
  About: {active: 'information-circle', inactive: 'information-circle-outline'},
};

function MainTabs() {
  return <Tab.Navigator screenOptions={({route}) => ({
    headerShown: false,
    tabBarActiveTintColor: colors.forest,
    tabBarInactiveTintColor: colors.muted,
    tabBarLabelStyle: {fontSize: 12, fontWeight: '700'},
    tabBarStyle: {height: 72, paddingBottom: 9, paddingTop: 7, borderTopColor: colors.border, backgroundColor: colors.white},
    tabBarIcon: ({focused, color, size}) => {
      const icon = tabIcons[route.name];
      return <Ionicons name={focused ? icon.active : icon.inactive} size={size + 2} color={color}/>;
    },
  })}>
    <Tab.Screen name="Home" component={HomeScreen}/>
    <Tab.Screen name="Ask" component={AskScreen}/>
    <Tab.Screen name="Directory" component={DirectoryScreen}/>
    <Tab.Screen name="About" component={AboutScreen}/>
  </Tab.Navigator>;
}

export default function App() { return <SafeAreaProvider><StatusBar style="dark"/><NavigationContainer><Stack.Navigator screenOptions={{headerTintColor: colors.forest, headerStyle: {backgroundColor: colors.cream}, headerShadowVisible: false}}><Stack.Screen name="Main" component={MainTabs} options={{headerShown: false}}/><Stack.Screen name="Result" component={ResultScreen} options={{title: 'AI result'}}/><Stack.Screen name="Profile" component={ProfileScreen} options={{title: 'Member profile'}}/></Stack.Navigator></NavigationContainer></SafeAreaProvider>; }

const styles = StyleSheet.create({
  heroLogoWrap: {height: 112, width: 150, alignSelf: 'center', alignItems: 'center', justifyContent: 'center', marginBottom: 4},
  heroGlowOuter: {position: 'absolute', width: 128, height: 82, borderRadius: 41, backgroundColor: '#B8E8A9', opacity: .28, transform: [{scale: 1.12}]},
  heroGlowInner: {position: 'absolute', width: 108, height: 72, borderRadius: 36, backgroundColor: colors.gold, opacity: .24},
  heroMark: {height: 70, minWidth: 100, paddingHorizontal: 18, borderRadius: 25, alignItems: 'center', justifyContent: 'center', backgroundColor: colors.forest, borderWidth: 2, borderColor: colors.gold, shadowColor: '#60D16F', shadowOffset: {width: 0, height: 0}, shadowOpacity: .9, shadowRadius: 18, elevation: 14},
  heroMarkText: {fontSize: 29, letterSpacing: 2.5, color: '#FFF5C7', fontWeight: '900', textShadowColor: '#EAFD9A', textShadowOffset: {width: 0, height: 0}, textShadowRadius: 10},
  factRow: {flexDirection: 'row', gap: 50, paddingVertical: 10}, fact: {fontSize: 22, fontWeight: '800', color: colors.ink, marginTop: 4},
  label: {fontSize: 13, color: colors.muted, fontWeight: '800', textTransform: 'uppercase', letterSpacing: .7}, input: {minHeight: 120, borderWidth: 1, borderColor: colors.border, borderRadius: 14, padding: 14, textAlignVertical: 'top', fontSize: 17, color: colors.ink, backgroundColor: colors.cream}, counter: {textAlign: 'right', color: colors.muted},
  error: {color: colors.danger, fontWeight: '600', lineHeight: 21}, notice: {padding: 12, borderRadius: 10, color: colors.forest, backgroundColor: colors.mint}, link: {fontSize: 15, lineHeight: 22, color: colors.green, fontWeight: '800'}, confidence: {alignSelf: 'flex-start', backgroundColor: colors.mint, color: colors.green, paddingHorizontal: 10, paddingVertical: 6, borderRadius: 999, fontWeight: '800'}, body: {fontSize: 15, lineHeight: 22, color: colors.ink}, bold: {fontWeight: '800'}, info: {gap: 3, paddingVertical: 3},
});
