import type { PropsWithChildren } from 'react';
import {ActivityIndicator, Pressable, ScrollView, StyleSheet, Text, View} from 'react-native';
import {colors} from './theme';

export function Page({children}: PropsWithChildren) {
  return <ScrollView style={styles.page} contentContainerStyle={styles.content} keyboardShouldPersistTaps="handled">{children}</ScrollView>;
}

export function Eyebrow({children}: PropsWithChildren) { return <Text style={styles.eyebrow}>{children}</Text>; }
export function Title({children}: PropsWithChildren) { return <Text style={styles.title}>{children}</Text>; }
export function Card({children}: PropsWithChildren) { return <View style={styles.card}>{children}</View>; }
export function SectionTitle({children}: PropsWithChildren) { return <Text style={styles.sectionTitle}>{children}</Text>; }
export function Muted({children}: PropsWithChildren) { return <Text style={styles.muted}>{children}</Text>; }
export function StatusPill({online}: {online: boolean}) {
  return <View style={[styles.pill, {backgroundColor: online ? colors.mint : '#FCEAE8'}]}><Text style={{color: online ? colors.green : colors.danger, fontWeight: '700'}}>{online ? '● Online' : '● Offline'}</Text></View>;
}
export function PrimaryButton({label, onPress, disabled = false, loading = false}: {label: string; onPress: () => void; disabled?: boolean; loading?: boolean}) {
  return <Pressable accessibilityRole="button" accessibilityLabel={label} disabled={disabled || loading} onPress={onPress} style={({pressed}) => [styles.button, (disabled || loading) && styles.disabled, pressed && styles.pressed]}>{loading ? <ActivityIndicator color={colors.white}/> : <Text style={styles.buttonText}>{label}</Text>}</Pressable>;
}

const styles = StyleSheet.create({
  page: {flex: 1, backgroundColor: colors.cream}, content: {padding: 20, paddingBottom: 42, gap: 16},
  eyebrow: {fontSize: 13, letterSpacing: 1.5, textTransform: 'uppercase', color: colors.green, fontWeight: '800'},
  title: {fontSize: 34, lineHeight: 39, fontWeight: '800', color: colors.ink},
  card: {backgroundColor: colors.white, borderRadius: 18, borderWidth: 1, borderColor: colors.border, padding: 18, gap: 10},
  sectionTitle: {fontSize: 20, lineHeight: 25, color: colors.ink, fontWeight: '800'},
  muted: {fontSize: 15, lineHeight: 22, color: colors.muted},
  pill: {alignSelf: 'flex-start', borderRadius: 999, paddingHorizontal: 12, paddingVertical: 7},
  button: {minHeight: 52, borderRadius: 14, backgroundColor: colors.forest, alignItems: 'center', justifyContent: 'center', paddingHorizontal: 18},
  buttonText: {color: colors.white, fontWeight: '800', fontSize: 16}, disabled: {opacity: .45}, pressed: {opacity: .82},
});

